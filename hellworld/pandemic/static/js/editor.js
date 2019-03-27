'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function make_post_request(url, content, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    // send the collected data as JSON
    xhr.send(JSON.stringify(content));

    xhr.onloadend = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            callback(json);
        }
    };
}

var EditorWindow = function (_React$Component) {
    _inherits(EditorWindow, _React$Component);

    function EditorWindow() {
        _classCallCheck(this, EditorWindow);

        return _possibleConstructorReturn(this, (EditorWindow.__proto__ || Object.getPrototypeOf(EditorWindow)).apply(this, arguments));
    }

    _createClass(EditorWindow, [{
        key: 'submit_code',
        value: function submit_code(e) {
            e.preventDefault();
            //make_post_request(code_submit_url, {"code": "#include <cstdio>\n int main(){printf(\"47\"); char a[1];  return 0;}", "language": 1, "task": 1})
            make_post_request(code_submit_url, { "code": "c = 0\nfor _ in range(10000):\n\tfor _ in range(1000):\n\t\tc+=1", "language": 0, "task": 1 });
        }
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'button',
                { onClick: this.submit_code },
                'Submit'
            );
        }
    }]);

    return EditorWindow;
}(React.Component);

var LogoutBtn = function (_React$Component2) {
    _inherits(LogoutBtn, _React$Component2);

    function LogoutBtn() {
        _classCallCheck(this, LogoutBtn);

        return _possibleConstructorReturn(this, (LogoutBtn.__proto__ || Object.getPrototypeOf(LogoutBtn)).apply(this, arguments));
    }

    _createClass(LogoutBtn, [{
        key: 'render',
        value: function render() {
            return React.createElement(
                'form',
                { method: 'post', action: logout_link },
                React.createElement('input', { type: 'submit', value: 'Logout' })
            );
        }
    }]);

    return LogoutBtn;
}(React.Component);

var TaskViewer = function (_React$Component3) {
    _inherits(TaskViewer, _React$Component3);

    function TaskViewer() {
        _classCallCheck(this, TaskViewer);

        return _possibleConstructorReturn(this, (TaskViewer.__proto__ || Object.getPrototypeOf(TaskViewer)).apply(this, arguments));
    }

    _createClass(TaskViewer, [{
        key: 'render',
        value: function render() {
            return React.createElement('embed', { src: task_pdf_link, type: 'application/pdf', width: '100%', height: '600px' });
        }
    }]);

    return TaskViewer;
}(React.Component);

var Editor = function (_React$Component4) {
    _inherits(Editor, _React$Component4);

    function Editor() {
        _classCallCheck(this, Editor);

        return _possibleConstructorReturn(this, (Editor.__proto__ || Object.getPrototypeOf(Editor)).apply(this, arguments));
    }

    _createClass(Editor, [{
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                null,
                React.createElement(EditorWindow, null),
                React.createElement(LogoutBtn, null)
            );
        }
    }]);

    return Editor;
}(React.Component);

$(document).ready(function () {
    var editor = ReactDOM.render(React.createElement(Editor, null), document.querySelector('#editor-container'));
});