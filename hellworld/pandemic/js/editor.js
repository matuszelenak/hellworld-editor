'use strict';

function make_post_request(url, content, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    // send the collected data as JSON
    xhr.send(JSON.stringify(content));

    xhr.onloadend = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let json = JSON.parse(xhr.responseText);
            callback(json);
        }
    };
}

class EditorWindow extends React.Component {


    submit_code(e) {
        e.preventDefault();
        make_post_request(code_submit_url, {"code": "somecodehere", "language": 1, "task": 1})
    }

    render() {
        return (
            <button onClick={this.submit_code}>Submit</button>
        );
    }
}

class LogoutBtn extends React.Component {
    render() {
        return (<form method="post" action={logout_link}><input type="submit" value="Logout" /></form>)
    }
}

class TaskViewer extends React.Component {
    render() {
        return (
            <embed src={task_pdf_link} type="application/pdf" width="100%" height="600px" />
        )
    }
}

class Editor extends React.Component {
    render() {
        return (
            <div>

                <EditorWindow/>
                <LogoutBtn/>
            </div>
        );
    }
}


$( document ).ready(function() {
    let editor = ReactDOM.render(<Editor/>, document.querySelector('#editor-container'));
});