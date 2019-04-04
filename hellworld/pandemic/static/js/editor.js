'use strict';

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var EditorWindow = function (_React$Component) {
    _inherits(EditorWindow, _React$Component);

    function EditorWindow(props) {
        _classCallCheck(this, EditorWindow);

        var _this = _possibleConstructorReturn(this, (EditorWindow.__proto__ || Object.getPrototypeOf(EditorWindow)).call(this, props));

        console.log(_this.props);
        _this.state = { code_value: '', language: 0 };

        _this.submitCode = _this.submitCode.bind(_this);
        _this.handleCodeChange = _this.handleCodeChange.bind(_this);
        _this.handleLanguageChange = _this.handleLanguageChange.bind(_this);
        return _this;
    }

    _createClass(EditorWindow, [{
        key: 'submitCode',
        value: function submitCode(e) {
            e.preventDefault();
            this.props.parent.submitCode({ code: this.state.code_value, language: this.state.language, task: 1 });
        }
    }, {
        key: 'handleCodeChange',
        value: function handleCodeChange(event) {
            this.setState({ code_value: event.target.value });
        }
    }, {
        key: 'handleLanguageChange',
        value: function handleLanguageChange(event) {
            this.setState({ language: event.target.value });
        }
    }, {
        key: 'render',
        value: function render() {
            var language_options = Object.entries(this.props.languages).map(function (_ref) {
                var _ref2 = _slicedToArray(_ref, 2),
                    key = _ref2[0],
                    value = _ref2[1];

                return React.createElement(
                    'option',
                    { value: value },
                    key
                );
            });

            return React.createElement(
                'div',
                null,
                React.createElement(
                    'select',
                    { onChange: this.handleLanguageChange },
                    language_options
                ),
                React.createElement(
                    'textarea',
                    { onChange: this.handleCodeChange },
                    'a'
                ),
                React.createElement(
                    'button',
                    { onClick: this.submitCode },
                    'Submit'
                )
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

    function Editor(props) {
        _classCallCheck(this, Editor);

        var _this4 = _possibleConstructorReturn(this, (Editor.__proto__ || Object.getPrototypeOf(Editor)).call(this, props));

        _this4.state = { active_diseases: [], rules: { languages: {} } };

        _this4.updateRules = _this4.updateRules.bind(_this4);
        _this4.submitCode = _this4.submitCode.bind(_this4);
        _this4.pollSubmitResult = _this4.pollSubmitResult.bind(_this4);

        return _this4;
    }

    _createClass(Editor, [{
        key: 'pollSubmitResult',
        value: function pollSubmitResult(id) {
            var _this5 = this;

            var url = submit_status_url.replace('4247', id);
            fetch(url).then(function (response) {
                return response.json();
            }).then(function (data) {
                if (data.status > 1) {
                    clearInterval(_this5.submit_result_timer);
                    //TODO add submit results to some list
                }
            });
        }
    }, {
        key: 'submitCode',
        value: function submitCode(data) {
            var _this6 = this;

            fetch(code_submit_url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            }).then(function (response) {
                return response.json();
            }).then(function (data) {
                console.log(data);
                _this6.submit_result_timer = setInterval(function () {
                    return _this6.pollSubmitResult(data.submit_id);
                }, 2000);
            });
        }
    }, {
        key: 'updateRules',
        value: function updateRules() {
            var _this7 = this;

            fetch(rules_url).then(function (results) {
                return results.json();
            }).then(function (data) {
                console.log(data);
                _this7.setState({ rules: data });
            });
        }
    }, {
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this8 = this;

            fetch(active_diseases_url).then(function (results) {
                return results.json();
            }).then(function (data) {
                console.log(data);
                _this8.setState({ active_diseases: data });
            });

            this.updateRules();
            this.rule_update_timer = setInterval(function () {
                return _this8.updateRules();
            }, 20000);
        }
    }, {
        key: 'componentWillUnmount',
        value: function componentWillUnmount() {
            clearInterval(this.rule_update_timer);
        }
    }, {
        key: 'render',
        value: function render() {
            console.log(this.state.rules);
            return React.createElement(
                'div',
                null,
                React.createElement(EditorWindow, { languages: this.state.rules.languages, parent: this }),
                React.createElement(LogoutBtn, null)
            );
        }
    }]);

    return Editor;
}(React.Component);

$(document).ready(function () {
    var editor = ReactDOM.render(React.createElement(Editor, null), document.querySelector('#editor-container'));
});