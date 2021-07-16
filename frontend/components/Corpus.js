import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
// import STYLES from "./Corpus.module.scss";
import {getCookie} from "../common";
import {Modal} from "react-bootstrap";

const Corpus = ({id}) => {

    const [corpusData, setCorpusData] = useState({});
    const [allDocData, setAllDocData] = useState([]);
    const [containsDoc, setContainsDoc] = useState({});
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const handleOpenModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);

    useEffect(() => {
        fetch(`/api/corpus/${id}`)
            .then(response => response.json())
            .then(data => {
                setCorpusData(data);
                fetch("/api/all_documents")
                    .then(response => response.json())
                    .then(docsData => {
                        setAllDocData(docsData);
                        docsData.map((doc) => setContainsDoc((values) => ({
                            ...values,
                            [doc.id]: data.documents.includes(doc.id)
                        })));
                        setLoading(false);
                    });
            });

    }, []);

    const handleCheckBoxChange = (event) => {
        setContainsDoc((values) => ({
            ...values,
            [event.target.id]: !containsDoc[event.target.id]
        }));
    };

    const updateDocs = (event) => {
        event.preventDefault();
        handleCloseModal();
        const docList = Object.keys(containsDoc).filter((id) => {
            return containsDoc[id];
        });
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                id: corpusData.id,
                documents: docList
            })
        };
        fetch("/api/update_corpus_docs", requestOptions)
            .then(response => response.json())
            .then(data => {
                setCorpusData(data);
            });
    };

    const docsList = () => {
        return (
            <>
                <h5>Documents:</h5>
                {
                    corpusData.documents.length
                        ? <ul>
                            {allDocData.map((doc, i) => {
                                if (corpusData.documents.includes(doc.id)) {
                                    return (
                                        <li key={i}>
                                            <i>{doc.title}</i>, by {doc.author} {doc.year &&
                                                `(${doc.year})`}
                                        </li>
                                    );
                                }
                            })}
                        </ul>
                        : <p><i>There are no documents in this corpus.</i></p>
                }

            </>
        );
    };

    const updateDocsList = () => {
        return (
            <>
                <button className="btn btn-outline-secondary"
                    onClick={handleOpenModal}>Update Documents</button>
                <Modal show={showModal} onHide={handleCloseModal}>
                    <Modal.Header closeButton>Update Documents</Modal.Header>
                    <form onSubmit={updateDocs}>
                        <Modal.Body>
                            {allDocData.map((doc, i) => (
                                <div key={i} className="custom-control custom-checkbox">
                                    <input type="checkbox"
                                        className="custom-control-input"
                                        id={doc.id} checked={containsDoc[doc.id]}
                                        onChange={handleCheckBoxChange}/>
                                    <label className="custom-control-label"
                                        htmlFor={doc.id}>
                                        <i>{doc.title}</i>, by {doc.author} {doc.year &&
                                            `(${doc.year})`}</label>
                                </div>
                            ))}
                        </Modal.Body>
                        <Modal.Footer>
                            <button className="btn btn-secondary"
                                onClick={handleCloseModal}>Close</button>
                            <button className="btn btn-primary" type="submit">Update</button>
                        </Modal.Footer>
                    </form>
                </Modal>

            </>
        );
    };

    return (
        <div className="container-fluid">
            {loading
                ? <p>Currently loading Corpus...</p>
                : <div>
                    <h1>Corpus: {corpusData.title}</h1>
                    <h5>Description</h5>
                    <p>{corpusData.description}</p>
                    {docsList()}
                    {updateDocsList()}
                </div>
            }
        </div>
    );
};

Corpus.propTypes = {
    id: PropTypes.number
};

export default Corpus;
