import React, {useEffect, useState} from "react";
import STYLES from "./Corpora.module.scss";
import {getCookie} from "../common";
import {Modal} from "react-bootstrap";

const Corpora = () => {
    const [corporaData, setCorporaData] = useState([]);
    const [newCorpusData, setNewCorpusData] = useState({
        "title": "",
        "description": ""
    });
    const [loading, setLoading] = useState(true);
    const [addingCorpus, setAddingCorpus] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);

    useEffect(() => {
        fetch("/api/all_corpora")
            .then(response => response.json())
            .then(data => {
                setCorporaData(data);
                setLoading(false);
            });
    }, []);

    const handleTitleInputChange = (event) => {
        setNewCorpusData((values) => ({
            ...values,
            title: event.target.value
        }));
    };

    const handleDescriptionInputChange = (event) => {
        setNewCorpusData((values) => ({
            ...values,
            description: event.target.value
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        setAddingCorpus(true);
        handleCloseModal();
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CRSFToken": csrftoken
            },
            body: JSON.stringify({
                title: newCorpusData.title,
                description: newCorpusData.description
            })
        };
        fetch("api/add_corpus", requestOptions)
            .then(response => response.json())
            .then(data => {
                setCorporaData(corporaData => [...corporaData, data]);
                setNewCorpusData({
                    "title": "",
                    "description": ""
                });
                setAddingCorpus(false);
            });
    };

    const addCorpusModal = () => {
        return (
            <>
                <button className="btn btn-primary mb-3"
                    onClick={handleShowModal}>Add Corpus</button>
                <Modal show={showModal} onHide={handleCloseModal}>
                    <Modal.Header closeButton>Add Corpus</Modal.Header>
                    <form onSubmit={handleSubmit}>
                        <Modal.Body>
                            <div className="row mb-3">
                                <label htmlFor="title"
                                    className="col-2 col-form-label">Title</label>
                                <div className="col">
                                    <input type="text" className="form-control"
                                        id="title" value={newCorpusData.title}
                                        onChange={handleTitleInputChange} required/>
                                </div>
                            </div>
                            <div className="row mb-3">
                                <label htmlFor="description"
                                    className="col form-label">Description</label>
                            </div>
                            <div className="row">
                                <div className="col">
                                    <textarea row="4" className="form-control"
                                        id="description" value={newCorpusData.description}
                                        onChange={handleDescriptionInputChange}/>
                                </div>
                            </div>
                        </Modal.Body>
                        <Modal.Footer>
                            <button className="btn btn-secondary"
                                onClick={handleCloseModal}>Close</button>
                            <button className="btn btn-primary" type="submit">Add</button>
                        </Modal.Footer>
                    </form>
                </Modal>
            </>
        );
    };

    const corporaList = () => {
        return (
            <>
                {corporaData.map((corpus, i) => (
                    <div className="col-6 mb-3" key={i}>
                        <a className={STYLES.corpusCard} href={`/corpus/${corpus.id}`}>
                            <div className="card">
                                <div className="card-body">
                                    <h2 className={STYLES.title}>{corpus.title}</h2>
                                    <p>{corpus.description}</p>
                                </div>
                            </div>
                        </a>
                    </div>
                ))}
            </>
        );
    };

    return(
        <div className="container-fluid">
            <h1>Corpora</h1>
            <p>
                This page displays all the corpora in the database.
            </p>
            {
                addingCorpus && <div className="alert alert-warning" role="alert">
                        Currently adding corpus...Please do not close this tab.
                </div>
            }
            {addCorpusModal()}
            {
                loading
                    ? <p>Currently loading Corpora...</p>
                    : <div>{corporaList()}</div>
            }
        </div>
    );
};

export default Corpora;
