import React, {useEffect, useState} from "react";
// import * as PropTypes from "prop-types";
// import STYLES from "./Documents.module.scss";

const Documents = () => {

    const [docData, setDocData] = useState(null);
    const [newDocData, setNewDocData] = useState({
        "author": "",
        "title":"",
        "data": null,
        "text": ""
    });

    useEffect(() => {
        fetch("/api/all_documents")
            .then(response => response.json())
            .then(data => {
                setDocData(data);
            });
    }, []);

    const handleTitleInputChange = (event) => {
	    event.persist();
	    setNewDocData((values) => ({
		    ...values,
		    title: event.target.value
	    }));
    };

    const handleDateInputChange = (event) => {
	    event.persist();
	    setNewDocData((values) => ({
		    ...values,
		    date: event.target.value
	    }));
    };

    const handleTextInputChange = (event) => {
	    event.persist();
	    setNewDocData((values) => ({
		    ...values,
		    text: event.target.value
	    }));
    };

    const handleAuthorInputChange = (event) => {
	    event.persist();
	    setNewDocData((values) => ({
		    ...values,
		    author: event.target.value
	    }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                title: newDocData.title,
                date: newDocData.date,
                author: newDocData.author,
                text: newDocData.text
            })
        };
        fetch("api/add_text", requestOptions)
            .then(response => response.json())
            .then(data => setDocData(docData => [...docData, data]));
    };

    return (
        <div>
            <h1>This is the Documents page.</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>

            <div>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="author">Author</label>
                        <input type="text" className="form-control"
                            id="author" value={newDocData.author}
                            onChange={handleAuthorInputChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="title">Title</label>
                        <input type="text" className="form-control"
                            id="title" value={newDocData.title}
                            onChange={handleTitleInputChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="date">Date</label>
                        <input type="text" className="form-control"
                            id="date" value={newDocData.date}
                            onChange={handleDateInputChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="text">Text</label>
                        <textarea className="form-control" id="text"
                            rows="8" value={newDocData.text}
                            onChange={handleTextInputChange}></textarea>
                    </div>
                    <button type="submit">Add</button>
                </form>
            </div>
            {
                docData
                    ? <div>Documents:
                        {docData.map((doc, i) => {
                            return (<>
                                <p>Document {i}</p>
                                <ul key={i}>
                                    {Object.keys(doc).map((key, i) => {
                                        return (
                                            <li key={i}>{key}: {doc[key]}</li>
                                        );
                                    })}
                                </ul>
                            </>
                            );
                        })}
                    </div>
                    : <p>Currently Loading Documents...</p>
            }
        </div>
    );
};

export default Documents;
