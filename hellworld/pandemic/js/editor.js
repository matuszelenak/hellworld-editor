'use strict';


class EditorWindow extends React.Component {
    render() {
        return (<p>Hello</p>);
    }
}

class LogoutBtn extends React.Component {
    render() {
        return (<form method="post" action={logout_link}><input type="submit" value="Logout" /></form>)
    }
}

class Editor extends React.Component {
    render() {
        return (
            <div><p>Hello World</p>
            <LogoutBtn/></div>
        );
    }
}


$( document ).ready(function() {
    let editor = ReactDOM.render(<Editor/>, document.querySelector('#editor-container'));
});