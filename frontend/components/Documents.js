import React, {useEffect, useState} from "react";
// import * as PropTypes from "prop-types";
// import STYLES from "./Documents.module.scss";
import {getCookie} from "../common";

const Documents = () => {

    const [docData, setDocData] = useState([]);
    const [newDocData, setNewDocData] = useState({
        "author": "",
        "title":"",
        "year": "",
        "text": ""
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("/api/all_documents")
            .then(response => response.json())
            .then(data => {
                setDocData(data);
                setLoading(false);
            });
    }, []);

    const handleTitleInputChange = (event) => {
	    setNewDocData((values) => ({
		    ...values,
		    title: event.target.value
	    }));
    };

    const handleYearInputChange = (event) => {
	    setNewDocData((values) => ({
		    ...values,
		    year: event.target.value
	    }));
    };

    const handleTextInputChange = (event) => {
	    setNewDocData((values) => ({
		    ...values,
		    text: event.target.value
	    }));
    };

    const handleAuthorInputChange = (event) => {
	    setNewDocData((values) => ({
		    ...values,
		    author: event.target.value
	    }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                title: newDocData.title,
                year: typeof newDocData.year === "string" ? null : newDocData.year,
                author: newDocData.author,
                text: newDocData.text
            })
        };
        fetch("api/add_text", requestOptions)
            .then(response => response.json())
            .then(data => {
                setDocData(docData => [...docData, data]);
                setNewDocData({
                    "author": "",
                    "title":"",
                    "year": "",
                    "text": ""
                });
            });
    };

    const docInfo = (doc, i) => {
        return (
            <ul> Document {i}
                {Object.keys(doc).map((attribute, i) => (
                    <li key={i}>{attribute}: {doc[attribute]}</li>
                ))}
            </ul>
        );
    };

    const docList = () => {
        return (
            <ul>
                {docData.map((doc, i) => (
                    <li key={i}> {docInfo(doc, i)} </li>
                ))}
            </ul>
        );
    };

    return (
        <div>
            <h1>This is the Documents page.</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>
            <form onSubmit={handleSubmit}>
                <label>
                    <p>Author</p>
                    <input type="text" className="form-control"
                        id="author" value={newDocData.author}
                        onChange={handleAuthorInputChange}/>
                </label>
                <label>
                    <p>Title</p>
                    <input type="text" className="form-control"
                        id="title" value={newDocData.title}
                        onChange={handleTitleInputChange}/>
                </label>
                <label>
                    <p>Year</p>
                    <input type="number" className="form-control"
                        id="year" value={newDocData.year}
                        max="9999"
                        onChange={handleYearInputChange}/>
                </label>
                <label>
                    <p>Text</p>
                    <textarea className="form-control" id="text"
                        rows="8" value={newDocData.text}
                        onChange={handleTextInputChange}></textarea>
                </label>
                <button type="submit">Add</button>
            </form>
            {
                loading
                    ? <p>Currently Loading Documents...</p>
                    : <div>
                        Documents:
                        {docList()}
                    </div>
            }
        </div>
    );
};

export default Documents;
