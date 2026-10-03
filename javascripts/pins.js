// 本地预览（mkdocs serve）时：分类页点选首页、首页移出、收集箱归档。线上只读，只保留首页复制。
(function () {
  "use strict";

  var LOCAL_HOSTS = ["localhost", "127.0.0.1", "[::1]"];
  var detecting = null;

  // 站点根地址，来自 Material 写在页面里的配置。
  function siteRoot() {
    var base = JSON.parse(document.getElementById("__config").textContent).base;
    return new URL(base.replace(/\/?$/, "/"), location.href);
  }

  function apiUrl(name) {
    return new URL("__" + name + "__", siteRoot()).href;
  }

  // 只在本机预览时探测接口，线上不发请求。
  function detectApi() {
    if (LOCAL_HOSTS.indexOf(location.hostname) === -1) {
      return Promise.resolve(false);
    }
    if (!detecting) {
      detecting = fetch(apiUrl("pins"), { cache: "no-store" })
        .then(function (response) { return response.ok ? response.json() : null; })
        .then(function (data) { return Boolean(data && data.ok); })
        .catch(function () { return false; });
    }
    return detecting;
  }

  function post(name, body) {
    return fetch(apiUrl(name), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) {
          throw new Error(data.error || response.statusText);
        }
        return data;
      });
    });
  }

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character];
    });
  }

  // ---------- 分类页：☆ / ★ ----------

  function showToggle(button, pinned) {
    var label = pinned ? "移出首页" : "加入首页";
    button.textContent = pinned ? "★" : "☆";
    button.title = label;
    button.setAttribute("aria-label", label);
    button.setAttribute("aria-pressed", String(pinned));
  }

  // 保存成功后预览会自动重建并刷新页面，这里先切换按钮状态。
  function addToggles() {
    document.querySelectorAll("h3[data-pin-id]").forEach(function (heading) {
      if (heading.querySelector(".pin-toggle")) {
        return;
      }
      var button = document.createElement("button");
      button.type = "button";
      button.className = "pin-toggle";
      showToggle(button, heading.hasAttribute("data-pinned"));
      button.addEventListener("click", function () {
        var next = button.getAttribute("aria-pressed") !== "true";
        button.disabled = true;
        post("pins", { id: heading.dataset.pinId, pinned: next })
          .then(function () { showToggle(button, next); })
          .catch(function (error) { alert("没有保存：" + error.message); })
          .finally(function () { button.disabled = false; });
      });
      heading.appendChild(button);
    });
  }

  // ---------- 首页：移出与复制 ----------

  function refreshCounts(column) {
    var count = column.querySelectorAll(".pin-item").length;
    column.querySelector(".pin-column-count").textContent = count;
    if (count === 0 && !column.querySelector(".pin-empty")) {
      column.querySelector(".pin-list").insertAdjacentHTML("beforeend", '<li class="pin-empty">暂无</li>');
    }
    var number = document.querySelector(".pin-number");
    if (number) {
      number.textContent = document.querySelectorAll(".pin-item").length;
    }
  }

  function enableRemove() {
    document.querySelectorAll(".pin-item .pin-remove").forEach(function (button) {
      button.hidden = false;
      button.addEventListener("click", function () {
        var item = button.closest(".pin-item");
        var column = item.closest(".pin-column");
        button.disabled = true;
        post("pins", { id: item.dataset.pinId, pinned: false })
          .then(function () {
            item.remove();
            refreshCounts(column);
          })
          .catch(function (error) {
            button.disabled = false;
            alert("没有保存：" + error.message);
          });
      });
    });
  }

  // 剪贴板接口被浏览器拒绝时，退回到选中文本再复制的旧方法。
  function copyWithSelection(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    var copied = document.execCommand("copy");
    area.remove();
    return copied ? Promise.resolve() : Promise.reject(new Error("复制失败"));
  }

  function copy(text) {
    var writing = navigator.clipboard
      ? navigator.clipboard.writeText(text)
      : Promise.reject(new Error("没有剪贴板接口"));
    return writing.catch(function () { return copyWithSelection(text); });
  }

  function bindCopy() {
    document.querySelectorAll(".pin-copy").forEach(function (button) {
      button.addEventListener("click", function () {
        var code = button.closest(".pin-item").querySelector(".pin-code code");
        copy(code.textContent).then(function () {
          button.classList.add("is-copied");
          setTimeout(function () { button.classList.remove("is-copied"); }, 1200);
        }).catch(function () {});
      });
    });
  }

  // ---------- 收集箱：归档到分类 ----------

  function pageOptions(pages) {
    var groups = {};
    var order = [];
    pages.forEach(function (page) {
      if (!groups[page.section]) {
        groups[page.section] = [];
        order.push(page.section);
      }
      groups[page.section].push(
        '<option value="' + escapeHtml(page.source) + '">' + escapeHtml(page.title) + "</option>"
      );
    });
    return '<option value="">选择子页…</option>' + order.map(function (section) {
      return '<optgroup label="' + escapeHtml(section) + '">' + groups[section].join("") + "</optgroup>";
    }).join("");
  }

  function recordForm(record, pages) {
    var fields = record.fields;
    var form = document.createElement("form");
    form.className = "inbox-card";
    form.innerHTML =
      '<p class="inbox-raw"><span class="inbox-date">' + escapeHtml(record.date || "无日期") + "</span>" +
        escapeHtml(record.text) + "</p>" +
      '<div class="inbox-fields">' +
        '<label class="inbox-code">命令<input name="code" required></label>' +
        '<label>作用（即标题）<input name="effect" required></label>' +
        '<label>来源<input name="source" placeholder="可省略，如 ls ← list"></label>' +
      "</div>" +
      '<p class="inbox-warning" hidden></p>' +
      '<div class="inbox-actions">' +
        '<select name="page" required aria-label="分类">' + pageOptions(pages) + "</select>" +
        '<select name="subsection" aria-label="小节" disabled><option value="">小节（可不选）</option></select>' +
        '<label class="inbox-pin"><input type="checkbox" name="pin" checked> ⭐ 加入首页</label>' +
        '<button type="submit" class="md-button md-button--primary">归档</button>' +
        '<button type="button" class="md-button inbox-delete">删除</button>' +
        '<details class="inbox-more"><summary>更多</summary>' +
          '<label>锚点<input name="anchor" pattern="[a-z][a-z0-9-]*" placeholder="留空自动生成"></label>' +
          '<label>代码语言<select name="language"><option value="">按分类自动</option>' +
            "<option>bash</option><option>text</option><option>python</option></select></label>" +
        "</details>" +
      "</div>";
    form.elements.code.value = fields.code;
    form.elements.effect.value = fields.effect;
    form.elements.source.value = fields.source;
    return form;
  }

  function recordItem(card) {
    var elements = card.form.elements;
    return {
      raw: card.record.raw,
      page: elements.page.value,
      subsection: elements.subsection.value === "" ? null : Number(elements.subsection.value),
      code: elements.code.value,
      effect: elements.effect.value,
      source: elements.source.value,
      scene: card.record.fields.scene,
      anchor: elements.anchor.value,
      language: elements.language.value,
      pin: elements.pin.checked,
    };
  }

  function markFiled(card, result) {
    var link = new URL(result.page.replace(/\.md$/, "/") + "#" + result.anchor, siteRoot()).href;
    card.done = true;
    card.form.classList.add("is-done");
    card.form.innerHTML = '<p class="inbox-done">已归档到 ' + escapeHtml(result.where) +
      "（#" + escapeHtml(result.anchor) + "）" + (card.pinned ? "，并加入首页。" : "。") +
      ' <a href="' + escapeHtml(link) + '">查看条目</a></p>';
  }

  function setBusy(cards, busy) {
    cards.forEach(function (card) {
      Array.prototype.forEach.call(card.form.elements, function (element) { element.disabled = busy; });
      card.form.elements.subsection.disabled = busy || !card.form.elements.page.value;
    });
  }

  // 一次提交多条；服务器全部检查通过才写入，所以失败时什么都不会改。
  function fileCards(cards, refresh) {
    cards.forEach(function (card) { card.pinned = card.form.elements.pin.checked; });
    var items = cards.map(recordItem);
    setBusy(cards, true);
    return post("inbox", { action: "file", items: items })
      .then(function (result) {
        result.filed.forEach(function (filed, index) { markFiled(cards[index], filed); });
        refresh();
      })
      .catch(function (error) {
        setBusy(cards, false);
        alert("没有保存：" + error.message);
      });
  }

  function bindCard(card, pages, anchors, existing, refresh) {
    var form = card.form;
    var byPage = {};
    pages.forEach(function (page) { byPage[page.source] = page; });

    // 只提醒不拦截：同一命令也可能有不同用法。
    var warning = form.querySelector(".inbox-warning");
    function checkDuplicate() {
      var match = existing[form.elements.code.value.trim()];
      warning.hidden = !match;
      warning.textContent = match ? "已有相同命令：" + match + "。不需要的话可以直接删除这条记录。" : "";
    }
    form.elements.code.addEventListener("input", checkDuplicate);
    checkDuplicate();

    form.elements.page.addEventListener("change", function () {
      var page = byPage[form.elements.page.value];
      var select = form.elements.subsection;
      select.innerHTML = '<option value="">小节（可不选）</option>' + (page ? page.subsections.map(function (name, index) {
        return '<option value="' + index + '">' + escapeHtml(name) + "</option>";
      }).join("") : "");
      select.disabled = !page;
      refresh();
    });

    form.elements.anchor.addEventListener("input", function () {
      var anchor = form.elements.anchor;
      anchor.setCustomValidity(anchors.has(anchor.value) ? "这个锚点已被其他条目使用" : "");
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (form.reportValidity()) {
        fileCards([card], refresh);
      }
    });

    form.querySelector(".inbox-delete").addEventListener("click", function () {
      if (!confirm("删除这条记录？内容不会归档到任何分类。")) {
        return;
      }
      setBusy([card], true);
      post("inbox", { action: "delete", raw: card.record.raw })
        .then(function () {
          card.done = true;
          card.form.classList.add("is-done");
          card.form.innerHTML = '<p class="inbox-done">已删除这条记录。</p>';
          refresh();
        })
        .catch(function (error) {
          setBusy([card], false);
          alert("没有删除：" + error.message);
        });
    });
  }

  function initInbox() {
    var holder = document.querySelector("[data-inbox-filing]");
    if (!holder) {
      return;
    }
    fetch(apiUrl("inbox"), { cache: "no-store" })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        // 本地可编辑时，用归档卡片代替原来的静态列表。
        holder.parentElement.querySelectorAll(":scope > ul").forEach(function (list) { list.hidden = true; });
        holder.hidden = false;
        if (!data.records.length) {
          holder.innerHTML = '<p class="inbox-empty">收集箱是空的。</p>';
          return;
        }
        holder.innerHTML =
          '<div class="inbox-toolbar"><p class="inbox-hint">共 ' + data.records.length +
          " 条记录。每条只需选分类，命令、作用、来源已从记录里填好，标题用作用，锚点自动生成。</p>" +
          '<button type="button" class="md-button md-button--primary inbox-all" disabled>全部归档</button></div>';
        var batch = holder.querySelector(".inbox-all");
        var anchors = new Set(data.anchors);
        var cards = [];

        function readyCards() {
          return cards.filter(function (card) { return !card.done && card.form.elements.page.value; });
        }

        function refresh() {
          var count = readyCards().length;
          batch.disabled = count === 0;
          batch.textContent = count ? "全部归档（已选分类 " + count + " 条）" : "全部归档";
        }

        batch.addEventListener("click", function () {
          var ready = readyCards();
          for (var index = 0; index < ready.length; index += 1) {
            if (!ready[index].form.reportValidity()) {
              return;
            }
          }
          fileCards(ready, refresh);
        });

        data.records.forEach(function (record) {
          var card = { record: record, form: recordForm(record, data.pages), done: false };
          cards.push(card);
          holder.appendChild(card.form);
          bindCard(card, data.pages, anchors, data.existing, refresh);
        });
      })
      .catch(function (error) {
        holder.hidden = false;
        holder.textContent = "收集箱读取失败：" + error.message;
      });
  }

  function init() {
    bindCopy();
    detectApi().then(function (editable) {
      if (!editable) {
        return;
      }
      document.body.classList.add("pins-editable");
      addToggles();
      enableRemove();
      initInbox();
    });
  }

  // Material 的 document$ 在每次页面加载（包括以后开启即时导航）时触发。
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
