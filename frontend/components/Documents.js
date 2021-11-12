import React, {useEffect, useState} from "react";
import STYLES from "./Documents.module.scss";
import {getCookie} from "../common";
import {Form, Modal, Row, Spinner} from "react-bootstrap";

const Documents = () => {

    const [docData, setDocData] = useState([]);
    const [newDocData, setNewDocData] = useState({
        "author": "",
        "title": "",
        "year": "",
        "text": ""
    });
    const [newAttributes, setNewAttributes] = useState([{"name": "", "value": ""}]);
    const [loading, setLoading] = useState(true);
    const [addingDoc, setAddingDoc] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);
    const [fileLoading, setFileLoading] = useState(false);

    const fileReader = new FileReader();
    fileReader.onload = (e) => {
       setNewDocData((values) => ({
            ...values,
            text: e.target.result
        }));
       fileReader.onloadstart = () => {
           setFileLoading(true);
        };
       fileReader.onloadend = () => {
           setFileLoading(false);
       };
    };

    const handleOnFileChange = e => {
        fileReader.readAsText(e.target.files[0]);
    };

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

    const handleAttributeInputChange = (event, index) => {
        const {name, value} = event.target;
        setNewAttributes(prevAttributes => {
            return prevAttributes.map((attribute, i) => {
                return i === index ? {...attribute, [name]: value} : attribute;
            });
        });
    };

    const handleAddAttribute = () => {
        setNewAttributes([...newAttributes, {"name": "", "value": ""}]);
    };

    const handleRemoveAttribute = (index) => {
        setNewAttributes(previousAttributes => (
            previousAttributes.filter((attribute, idx) => idx !== index)
        ));
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
                year: newDocData.year,
                author: newDocData.author,
                text: newDocData.text,
                newAttributes: newAttributes
            })
        };
        fetch("api/add_document", requestOptions)
            .then(response => response.json())
            .then(data => {
                setDocData(docData => [...docData, data]);
                setNewDocData({
                    "author": "",
                    "title": "",
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
                            {doc.author ? doc.author : "Unknown"}
                            <br/>
                            Year Published: {doc.year ? doc.year : "Unknown"}
                            <br/>
                            Word Count: {doc.word_count.toLocaleString()}
                        </p>

                    </div>
                </div>
            </a>
        );
    };

    const docList = () => {
        return (
            <div className="row">
                {docData.map((doc, i) => (
                    <div className="col-6 mb-3" key={i}>
                        {docInfo(doc, i)}
                    </div>
                ))}
            </div>
        );
    };

    const addDocModal = () => {
        return (
            <>
                <button className="btn btn-primary mb-3"
                        onClick={handleShowModal}>Add Document
                </button>
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
                                           onChange={handleTitleInputChange} required/>
                                </div>
                            </div>
                            <div className="row mb-3">
                                <label htmlFor="year" className="col-2 col-form-label">Year</label>
                                <div className="col">
                                    <input type="number" className="form-control"
                                           id="year" value={newDocData.year}
                                           max="9999"
                                           onKeyDown={e => (e.key === "e" || e.key === ".") &&
                                               e.preventDefault()}
                                           onChange={handleYearInputChange}/>
                                </div>
                            </div>
                            <>
                            </>
                            <div className="row mb-3">
                                <label htmlFor="text" className="col-2 col-form-label">Text</label>
                                <div className="col">
                                    <textarea className="form-control" id="text"
                                              rows="8" value={newDocData.text}
                                              onChange={handleTextInputChange} required/>
                                </div>
                            </div>
                            <Row className="ml-2">
                                <Form.Group controlId="formFile" className="mb-3" onChange={handleOnFileChange}>
                                    <Form.Control type="file" accept="text/*"/>
                                </Form.Group>
                                {fileLoading && <Spinner animation="border" role="status"/>}
                            </Row>
                            <p>Attributes</p>
                            {
                                newAttributes.map((attribute, i) => {
                                    return (
                                        <div key={i} className="row mb-3">
                                            <div className="col-4">
                                                <input type="text" className="form-control"
                                                       name="name" onChange={event =>
                                                    handleAttributeInputChange(event, i)}
                                                       placeholder="name" value={attribute.name}
                                                       required={!!newAttributes[i]["value"]}/>
                                            </div>
                                            <div className="col-3">
                                                <input type="text" className="form-control"
                                                       name="value" onChange={event =>
                                                    handleAttributeInputChange(event, i)}
                                                       placeholder="value" value={attribute.value}
                                                       required={!!newAttributes[i]["name"]}/>
                                            </div>
                                            {newAttributes.length !== 1 &&
                                            <div className="col">
                                                <button type="button"
                                                        onClick={() => handleRemoveAttribute(i)}
                                                        className="btn btn-secondary">
                                                    Remove
                                                </button>
                                            </div>}
                                            {newAttributes.length - 1 === i &&
                                            <div className="col">
                                                <button type="button"
                                                        onClick={handleAddAttribute}
                                                        className="btn btn-primary">Add
                                                </button>
                                            </div>}
                                        </div>
                                    );
                                })
                            }
                        </Modal.Body>
                        <Modal.Footer>
                            <button className="btn btn-secondary" type="button"
                                    onClick={handleCloseModal}>Close
                            </button>
                            <button className="btn btn-primary"
                                    type="submit">Add
                            </button>
                        </Modal.Footer>
                    </form>
                </Modal>
            </>
        );
    };

    return (
        <div className="container-fluid">
            <h1>Documents</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>
            {addingDoc && <div className="alert alert-warning" role="alert">
                Currently adding document... Please do not close this tab.
            </div>
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
