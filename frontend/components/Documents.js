import React, {useEffect, useState} from "react";
// import * as PropTypes from "prop-types";
import STYLES from "./Documents.module.scss";
import {getCookie} from "../common";
import {Modal} from "react-bootstrap";

const Documents = () => {

    const [docData, setDocData] = useState([]);
    const [newDocData, setNewDocData] = useState({
        "author": "",
        "title":"",
        "year": "",
        "text": ""
    });
    const [loading, setLoading] = useState(true);
    const [addingDoc, setAddingDoc] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);

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
        setAddingDoc(true);
        handleCloseModal();
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
        fetch("api/add_document", requestOptions)
            .then(response => response.json())
            .then(data => {
                setDocData(docData => [...docData, data]);
                setNewDocData({
                    "author": "",
                    "title":"",
                    "year": "",
                    "text": ""
                });
                setAddingDoc(false);
            });
    };

    const docInfo = (doc) => {
        return (
            <a href={`/document/${doc.id}`} className={STYLES.docCard}>
                <div className="card">
                    <div className="card-body">
                        <h6 className="mb-0">{doc.title}</h6>
                        <p>
                            {doc.author}
                            <br/>
                            Year Published: {doc.year ? doc.year : "Unknown"}
                            <br/>
                            Word Count: {doc.word_count}
                        </p>

                    </div>
                </div>
            </a>
        );
    };

    const docList = () => {
        return (
            <div className="container-fluid">
                <div className="row">
                    {docData.map((doc, i) => (
                        <div className="col-6 mb-3" key={i}>
                            {docInfo(doc, i)}
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    const addDocModal = () => {
        return (
            <>
                <button className="btn btn-primary mb-3"
                    onClick={handleShowModal}>Add Document</button>
                <Modal show={showModal} onHide={handleCloseModal}>
                    <Modal.Header closeButton>Add Document</Modal.Header>
                    <form onSubmit={handleSubmit}>
                        <Modal.Body>
                            <div className="row mb-3">
                                <label htmlFor="author"
                                    className="col-2 col-form-label">Author</label>
                                <div className="col">
                                    <input type="text" className="form-control"
                                        id="author" value={newDocData.author}
                                        onChange={handleAuthorInputChange}/>
                                </div>
                            </div>
                            <div className="row mb-3">
                                <label htmlFor="title"
                                    className="col-2 col-form-label">Title</label>
                                <div className="col">
                                    <input type="text" className="form-control"
                                        id="title" value={newDocData.title}
                                        onChange={handleTitleInputChange}/>
                                </div>
                            </div>
                            <div className="row mb-3">
                                <label htmlFor="year" className="col-2 col-form-label">Year</label>
                                <div className="col">
                                    <input type="number" className="form-control"
                                        id="year" value={newDocData.year}
                                        max="9999"
                                        onKeyDown={ e => ( e.key === "e" || e.key === "." ) &&
                                            e.preventDefault() }
                                        onChange={handleYearInputChange}/>
                                </div>
                            </div>
                            <div className="row mb-3">
                                <label htmlFor="text" className="col-2 col-form-label">Text</label>
                                <div className="col">
                                    <textarea className="form-control" id="text"
                                        rows="8" value={newDocData.text}
                                        onChange={handleTextInputChange} required></textarea>
                                </div>
                            </div>
                        </Modal.Body>
                        <Modal.Footer>
                            <button className="btn btn-secondary"
                                onClick={handleCloseModal}>Close</button>
                            <button className="btn btn-primary"
                                type="submit">Add</button>
                        </Modal.Footer>
                    </form>
                </Modal>
            </>
        );
    };

    return (
        <div>
            <h1>Documents</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>
            {
                addingDoc
                    ? <div className="alert alert-warning" role="alert">
                        Currently adding document... Please do not close this tab.
                    </div>
                    : null
            }
            {addDocModal()}
            {
                loading
                    ? <p>Currently Loading Documents...</p>
                    : <div>
                        {docList()}
                    </div>
            }
        </div>
    );
};

export default Documents;
