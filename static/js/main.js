/*
 * @Author: qwelz
 * @Date: 2021-03-19 14:45:26
 * @LastEditors: qwelz
 * @LastEditTime: 2021-03-19 14:54:19
 */

/**
 * JavaScript Date 格式化
 */
Date.prototype._pad_2 = (num) => (num < 10 ? "0" + num : "" + num);

Date.prototype.toDateString = function () {
    return [
        this.getFullYear(),
        this._pad_2(this.getMonth() + 1),
        this._pad_2(this.getDate()),
    ].join("-");
};

Date.prototype.toTimeString = function () {
    return [
        this._pad_2(this.getHours()),
        this._pad_2(this.getMinutes()),
        this._pad_2(this.getSeconds()),
    ].join(":");
};

Date.prototype.toDateTimeString = function () {
    return `${this.toDateString()} ${this.toTimeString()}`;
};


/**
 * 右侧信息框
 */
class MessagesBoxController {
    constructor() {
        this.container = $(".right-content .messages-container.row");
    }

    __divide_line(text) {
        return $(`
            <div class="col-md-12 time-divide-line">
                <div>${text}</div>
            </div>
        `);
    }

    __user_message(message) {
        const result = this.__received_message(message);
        result.addClass("from-me");
        return result;
    }

    __received_message(message) {
        const datetime = new Date(message.timestamp * 1000).toDateTimeString();
        return $(`
            <div class="col-md-12 message-box">
                <div class="message-header">
                    <div class="user-name">${message.user_name}</div>
                    <div class="time-label">${datetime}</div>
                </div>
                <div class="message-content col-md-6 col-sm-6 col-xs-6">${message.text}</div>
            </div>
        `);
    }

    _clear_old_divide_lines() {
        this.container.find(".clearable.time-divide-line").remove();
    }

    _scroll_to_bottom() {
        $(document).scrollTop($(document).height());
    }

    _append_messages(messages) {
        const that = this;
        messages.forEach(message => {
            that.container.append(
                PY_DATA["user_name"] === message["user_name"]
                    ? that.__user_message(message)
                    : that.__received_message(message)
            );
        });
        this._scroll_to_bottom();
    }


    change_title(name) {
        return $(".right-content nav a").text(name);
    }

    append_divide_line(text = null, clearable = true) {
        const result = this.__divide_line(text === null ? "以下为新消息" : text);
        this.container.append(result);
        if (clearable) {
            result.addClass("clearable");
        }
        return result;
    }

    append_self_message(message) {
        // 先清空
        $("#send-message-form input:text").val("");
        this._clear_old_divide_lines();
        // 再填充
        this._append_messages([message])
    }

    fresh(messages) {
        this._clear_old_divide_lines();
        this.append_divide_line();
        this._append_messages(messages);
    }

    refresh(messages) {
        $(".input-container.row").show();
        // 先清空
        $("#send-message-form input:text").val("");
        this.container.html("");
        // 再填充
        this._append_messages(messages);
    }
}

const RIGHT = new MessagesBoxController();

function append_left_tab(name) {
    const tab = $(`
        <li data-name="${name}" class="list-group-item d-flex justify-content-between align-items-center">
            ${name}
            <span class="badge badge-primary badge-pill" style="display: none;"></span>
        </li>
    `);
    $(".left-menu ul.list-group").append(tab).find("li").each(function () {
        $(this).removeClass("active");
    });
    tab.addClass("active");
}

// 添加群聊
$("#add-group-confirm-button").click(function () {
    const name = $("#group-name-input").val();
    if ($(`.group-tab[data-name='${name}']`).length > 0) {
        alert("已加入此群聊");
        return null;
    }

    $.post("/groups/get-messages", {
        "group": name,
    }).done(function (data) {
        // 左侧添加群聊 tab
        append_left_tab(name);
        // 更新右侧的聊天内容
        PY_DATA["group"] = name;
        RIGHT.change_title(name);
        RIGHT.refresh(data.messages);
        // 关闭 modal
        $("#join-chat-group-modal").modal("hide");
    }).fail(function () {
        alert("加入群聊失败");
    });
});

// 发送消息
$("#send-message-form").submit(function (e) {
    e.preventDefault();
    const message_text = $(this).find("input:text").val().trim();
    if (message_text === "") {
        return null;
    }

    $.post("/groups/send-message", {
        "group": PY_DATA["group"],
        "text": message_text,
    }).done(function (data) {
        if (!data.status) {
            return alert("请求数据为空");
        }
        RIGHT.append_self_message(data.message);
    }).fail(function () {
        alert("发送消息失败");
    });
});


// 建立 websocket 连接
const WS = new WebSocket(`ws://${window.location.host}/websocket`);
WS.onmessage = function (e) {
    const data = JSON.parse(e.data);
    RIGHT.fresh(Object.values(data.messages));
};