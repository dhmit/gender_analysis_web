import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "./Corpus.module.scss";
import {NLTK_TAGS, PRONOUN_TYPES, getCookie, sortResults} from "../common";
import {Modal, OverlayTrigger, Tooltip} from "react-bootstrap";

const Corpus = ({id}) => {

    const [corpusData, setCorpusData] = useState({});
    const [allDocData, setAllDocData] = useState([]);
    const [containsDoc, setContainsDoc] = useState({});
    const [loadingCorpus, setLoadingCorpus] = useState(true);
    const [loadingDocs, setLoadingDocs] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const handleOpenModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);

    const [runningProximityAnalysis, setRunningProximityAnalysis] = useState(false);
    const [wordWindow, setWordWindow] = useState(2);
    const [ProximityAnalysisResults, setProximityAnalysisResults] = useState({});
    const [showProximityModal, setShowProximityModal] = useState(false);
    const handleShowProximityModal = () => setShowProximityModal(true);
    const handleCloseProximityModal = () => setShowProximityModal(false);
    const handleWordWindowChange = (event) => {
        event.target.value && setWordWindow(parseInt(event.target.value));
    };

    useEffect(() => {
        fetch(`/api/corpus/${id}`)
            .then(response => response.json())
            .then(data => {
                setCorpusData(data);
                setLoadingCorpus(false);
                fetch("/api/all_documents")
                    .then(response => response.json())
                    .then(docsData => {
                        setAllDocData(docsData);
                        docsData.forEach((doc) => setContainsDoc((values) => ({
                            ...values,
                            [doc.id]: data.documents.includes(doc.id)
                        })));
                        setLoadingDocs(false);
                    });
            });

    }, []);

    const handleCheckBoxChange = (event) => {
        setContainsDoc((values) => ({
            ...values,
            [event.target.id]: !containsDoc[event.target.id]
        }));
    };

    const addProximityModal = () => {
        return (
            <>
                <button className="btn btn-danger btn-sm" onClick={handleShowProximityModal}>
                    Run Proximity Analysis
                </button>
                <Modal show={showProximityModal} onHide={handleCloseProximityModal}>
                    <Modal.Header closeButton>Proximity Analysis</Modal.Header>
                    <form onSubmit={handleProximitySubmit}>
                        <Modal.Body>

                            <div className="row mb-3">
                                <label htmlFor="word_window"
                                    className="col form-label">Please Enter A Word Window: </label>
                            </div>

                            <div className="row">
                                <div className="col">
                                    <input className="form-control"
                                        id="word_window" type="number" value={wordWindow}
                                        min="1"
                                        placeholder={"Ex: 2"}
                                        onChange={handleWordWindowChange}
                                    />
                                </div>
                            </div>
                        </Modal.Body>
                        <Modal.Footer>
                            <button className="btn btn-secondary"
                                onClick={handleCloseProximityModal}>Close</button>
                            <button className="btn btn-primary" type="submit">Run Analysis</button>
                        </Modal.Footer>
                    </form>
                </Modal>
            </>
        );

    };

    const handleProximitySubmit = event => {
        event.preventDefault();

        setRunningProximityAnalysis(true);
        handleCloseProximityModal();
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                corpus_id: id,
                word_window: wordWindow
            })
        };
        fetch("/api/proximity", requestOptions)
            .then(response => response.json())
            .then(data => {
                setProximityAnalysisResults(data.results);
                setRunningProximityAnalysis(false);
            });
    };

    const ProximityResultsDisplay = () => {
        return (
            <><h2 className={STYLES.title}>Proximity Analysis Results:</h2><dl>
                {Object.entries(ProximityAnalysisResults).map(docData => (
                    <><dl>
                        <dt className={STYLES.subtitle}><i>{docData[0]}</i></dt>
                        <dd><ul>
                            {Object.entries(docData[1]).sort().map(genderData => (
                                <><li><dl>
                                    <dt className={STYLES.eachGender}>{genderData[0]}</dt>
                                    <dd><ul>
                                        {Object.entries(genderData[1]).map(pronounData => (
                                            <><li><dl>
{/* eslint-disable-next-line max-len */}
                                                <dt className={STYLES.eachPronounType}>{PRONOUN_TYPES[pronounData[0]]}</dt>
                                                <dd><ul>
                                                    {Object.entries(pronounData[1]).map(posTags => (
                                                        <><li><dl>
                                                            <dt>{NLTK_TAGS[posTags[0]]}</dt>
                                                            <dd><ul>
{/* eslint-disable-next-line max-len */}
                                                                {Object.entries(posTags[1]).sort(sortResults).slice(0, 10)
                                                                    .map((wordFreq, i) => (
                                                                        <li key={i}>
{/* eslint-disable-next-line max-len */}
                                                                            {`${wordFreq[0]}: ${wordFreq[1]}`}
                                                                        </li>
                                                                    ))}
                                                            </ul></dd>
                                                        </dl></li></>
                                                    ))}
                                                </ul></dd>
                                            </dl></li></>
                                                    
                                        ))}
                                    </ul></dd>
                                </dl></li></>
                            ))}
                        </ul></dd>
                    </dl></>
                ))}
            </dl></>
        );
    };
    

    const updateDocs = (event) => {
        event.preventDefault();
        handleCloseModal();
        setLoadingDocs(true);
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
                setLoadingDocs(false);
            });
    };

    const docsList = () => {
        const docsInCorpus = allDocData.filter(doc => corpusData.documents.includes(doc.id));
        return (
            <>
                {corpusData.documents.length
                    ? <ul>
                        {docsInCorpus.map((doc, i) => (
                            <li key={i}>
                                <i>{doc.title}</i>, by {doc.author || "Anonymous"} {doc.year &&
                                    `(${doc.year})`}
                            </li>
                        ))}
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
            {loadingCorpus
                ? <p>Currently loading Corpus&hellip;</p>
                : <div>
                    <h1>Corpus: {corpusData.title}</h1>
                    <h2 className={STYLES.title}>Description</h2>
                    <p>{corpusData.description}</p>
                    <h2 className={STYLES.title}>Documents:</h2>

                    {loadingDocs
                        ? <p>Currently loading documents list&hellip;</p>
                        : <>
                            {docsList()} {updateDocsList()}
                        </>
                    }
                    <br/>
                    <br/>
                    <OverlayTrigger
                        overlay={<Tooltip>Run Proximity Analysis</Tooltip>}>
                        {addProximityModal}
                    </OverlayTrigger>
                    {runningProximityAnalysis &&
                        <p className="alert alert-warning" role="alert">
                            Currently running proximity analysis&hellip;
                            Please do not close this tab.
                        </p>
                    }
                    {ProximityAnalysisResults && ProximityResultsDisplay()}
                </div>
            }
        </div>
    );
};



Corpus.propTypes = {
    id: PropTypes.number
};

export default Corpus;
