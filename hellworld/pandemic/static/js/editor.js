'use strict';

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var EditorWindowCharacter = function (_React$Component) {
    _inherits(EditorWindowCharacter, _React$Component);

    function EditorWindowCharacter(props) {
        _classCallCheck(this, EditorWindowCharacter);

        var _this = _possibleConstructorReturn(this, (EditorWindowCharacter.__proto__ || Object.getPrototypeOf(EditorWindowCharacter)).call(this, props));

        console.log(_this.props.value);
        _this.state = { value: _this.props.value, parent_row: _this.props.parent_row };
        _this.handleMouseDown = _this.handleMouseDown.bind(_this);
        return _this;
    }

    _createClass(EditorWindowCharacter, [{
        key: 'handleMouseDown',
        value: function handleMouseDown(e) {
            console.log(this.props.index);
            this.state.parent_row.changeCursorPosition(this.props.index);
        }
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                { className: 'editor-char', onClick: this.handleMouseDown },
                this.state.value,
                this.props.index,
                ' '
            );
        }
    }]);

    return EditorWindowCharacter;
}(React.Component);

var EditorWindowRow = function (_React$Component2) {
    _inherits(EditorWindowRow, _React$Component2);

    function EditorWindowRow(props) {
        _classCallCheck(this, EditorWindowRow);

        var _this2 = _possibleConstructorReturn(this, (EditorWindowRow.__proto__ || Object.getPrototypeOf(EditorWindowRow)).call(this, props));

        _this2.state = { character_values: _this2.props.value.split('') };
        _this2.handleKeyPress = _this2.handleKeyPress.bind(_this2);
        _this2.changeCursorPosition = _this2.changeCursorPosition.bind(_this2);
        _this2.cursor_position = 0;
        return _this2;
    }

    _createClass(EditorWindowRow, [{
        key: 'changeCursorPosition',
        value: function changeCursorPosition(clicked_child_id) {
            ///this.cursor_position = this.characters.findIndex((ch) => ch.props.id === clicked_child_id);
            this.cursor_position = clicked_child_id;
            console.log(this.cursor_position);
        }
    }, {
        key: 'handleKeyPress',
        value: function handleKeyPress(e) {
            if (e.keyCode !== 13 && e.key !== 8) {
                var character_values = [].concat(_toConsumableArray(this.state.character_values));
                character_values.splice(this.cursor_position, 0, e.key);
                this.setState({ character_values: character_values });
                console.log(this.state);
            }
        }
    }, {
        key: 'componentDidMount',
        value: function componentDidMount() {
            document.addEventListener("keydown", this.handleKeyPress, false);
        }
    }, {
        key: 'componentWillUnmount',
        value: function componentWillUnmount() {
            document.removeEventListener("keydown", this.handleKeyPress, false);
        }
    }, {
        key: 'getContent',
        value: function getContent() {
            return this.state.character_values.reduce(function (acc, c) {
                return acc + c;
            }, "");
        }
    }, {
        key: 'render',
        value: function render() {
            var _this3 = this;

            return React.createElement(
                'div',
                { className: 'editor-row' },
                this.state.character_values.map(function (c, i) {
                    return React.createElement(EditorWindowCharacter, { index: i, value: c, parent_row: _this3 });
                })
            );
        }
    }]);

    return EditorWindowRow;
}(React.Component);

var EditorWindow = function (_React$Component3) {
    _inherits(EditorWindow, _React$Component3);

    function EditorWindow(props) {
        _classCallCheck(this, EditorWindow);

        var _this4 = _possibleConstructorReturn(this, (EditorWindow.__proto__ || Object.getPrototypeOf(EditorWindow)).call(this, props));

        _this4.state = { code_value: '', language: 0, row_values: ['Hello World', 'Please work'] };
        _this4.rows = [];

        _this4.submitCode = _this4.submitCode.bind(_this4);
        _this4.handleCodeChange = _this4.handleCodeChange.bind(_this4);
        _this4.handleLanguageChange = _this4.handleLanguageChange.bind(_this4);
        return _this4;
    }

    _createClass(EditorWindow, [{
        key: 'getContent',
        value: function getContent() {
            return this.rows.reduce(function (acc, r) {
                return acc + '\n' + r.getContent();
            }, "");
        }
    }, {
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
            this.rows = this.state.row_values.map(function (r) {
                return React.createElement(EditorWindowRow, { value: r });
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
                    'div',
                    null,
                    this.rows
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

var LogoutBtn = function (_React$Component4) {
    _inherits(LogoutBtn, _React$Component4);

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

var TaskViewer = function (_React$Component5) {
    _inherits(TaskViewer, _React$Component5);

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

var SubmitList = function (_React$Component6) {
    _inherits(SubmitList, _React$Component6);

    function SubmitList(props) {
        _classCallCheck(this, SubmitList);

        var _this7 = _possibleConstructorReturn(this, (SubmitList.__proto__ || Object.getPrototypeOf(SubmitList)).call(this, props));

        _this7.state = { submits: _this7.props.submits };
        return _this7;
    }

    _createClass(SubmitList, [{
        key: 'componentWillReceiveProps',
        value: function componentWillReceiveProps(nextProps) {
            this.setState({ submits: nextProps.submits });
        }
    }, {
        key: 'render',
        value: function render() {
            var submits = this.state.submits.map(function (submit) {
                return React.createElement(
                    'div',
                    null,
                    submit.id,
                    ': ',
                    submit.status
                );
            });
            return React.createElement(
                'div',
                null,
                submits
            );
        }
    }]);

    return SubmitList;
}(React.Component);

var Editor = function (_React$Component7) {
    _inherits(Editor, _React$Component7);

    function Editor(props) {
        _classCallCheck(this, Editor);

        var _this8 = _possibleConstructorReturn(this, (Editor.__proto__ || Object.getPrototypeOf(Editor)).call(this, props));

        _this8.state = { submits: [], active_diseases: [], rules: { languages: {} } };

        _this8.updateRules = _this8.updateRules.bind(_this8);
        _this8.submitCode = _this8.submitCode.bind(_this8);
        _this8.pollSubmitResult = _this8.pollSubmitResult.bind(_this8);

        return _this8;
    }

    _createClass(Editor, [{
        key: 'handleKeyPress',
        value: function handleKeyPress(e) {
            console.log(e);
        }
    }, {
        key: 'pollSubmitResult',
        value: function pollSubmitResult(id) {
            var _this9 = this;

            var url = submit_status_url.replace('4247', id);
            fetch(url).then(function (response) {
                return response.json();
            }).then(function (data) {
                if (data.status > 1) {
                    clearInterval(_this9.submit_result_timer);
                    var submits_copy = [].concat(_toConsumableArray(_this9.state.submits));
                    var submit_index = submits_copy.findIndex(function (x) {
                        return x.id === id;
                    });
                    var submit = _this9.state.submits[submit_index];
                    submit.status = data.status;
                    _this9.setState({
                        submits: submits_copy
                    });
                }
            });
        }
    }, {
        key: 'submitCode',
        value: function submitCode(data) {
            var _this10 = this;

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
                _this10.submit_result_timer = setInterval(function () {
                    return _this10.pollSubmitResult(data.submit_id);
                }, 2000);
                _this10.setState({
                    submits: [{ id: data.submit_id, status: 'Waiting' }].concat(_toConsumableArray(_this10.state.submits))
                });
            });
        }
    }, {
        key: 'updateRules',
        value: function updateRules() {
            var _this11 = this;

            fetch(rules_url).then(function (results) {
                return results.json();
            }).then(function (data) {
                console.log(data);
                _this11.setState({ rules: data });
            });
        }
    }, {
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this12 = this;

            fetch(active_diseases_url).then(function (results) {
                return results.json();
            }).then(function (data) {
                console.log(data);
                _this12.setState({ active_diseases: data });
            });

            this.updateRules();
            this.rule_update_timer = setInterval(function () {
                return _this12.updateRules();
            }, 2000000);
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
                React.createElement(SubmitList, { submits: this.state.submits }),
                React.createElement(LogoutBtn, null)
            );
        }
    }]);

    return Editor;
}(React.Component);

$(document).ready(function () {
    var editor = ReactDOM.render(React.createElement(Editor, null), document.querySelector('#editor-container'));
});