import React, {useState} from "react";
import * as PropTypes from "prop-types";
import {getCookie} from "../common";
import {Alert, Modal, OverlayTrigger, Tooltip} from "react-bootstrap";
import CollapsibleTree from "./CollapsibleTree";
import ReactJson from "react-json-view";


const Proximity = ({id}) => {
    const [runningProximityAnalysis, setRunningProximityAnalysis] = useState(false);
    const [wordWindow, setWordWindow] = useState(2);
    const [proximityAnalysisResults, setProximityAnalysisResults] = useState({});
    const [showProximityModal, setShowProximityModal] = useState(false);
    const handleShowProximityModal = () => setShowProximityModal(true);
    const handleCloseProximityModal = () => setShowProximityModal(false);
    const handleWordWindowChange = (event) => {
        event.target.value && setWordWindow(parseInt(event.target.value));
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
                                    onClick={handleCloseProximityModal} type="reset">Close
                            </button>
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

    const getD3ProximityAnalysisResultsHelper = (obj) => {
        if (typeof obj === "number") {
            return {"name": obj, "children": []};
        } else {
            return Object.keys(obj).map(key => ({
                "name": key,
                "children": getD3ProximityAnalysisResultsHelper(obj[key])
            }));
        }
    };

    const corpusNotSelectedWarning = () => {
        return (<Alert key='select-corpus-id' variant='danger'>
            Please select a corpus.
        </Alert>);
    };


    const getD3ProximityAnalysisResults = (obj) => {
        if (Object.keys(obj).length === 0) {
            return null;
        } else {
            return {"name": "Proximity Analysis", "children": getD3ProximityAnalysisResultsHelper(obj)};
        }
    };

    const ProximityResultsDisplay = () => {
        // return (<CollapsibleTree data={getD3ProximityAnalysisResults(ProximityAnalysisResults)}/>);
        return (<div> <br/> <ReactJson src={proximityAnalysisResults} collapsed={true} name={"results"}/></div>);
    };

    return (
        (id === -1) ? corpusNotSelectedWarning() :
        <div className="container-fluid">
            {<div>
                {<><OverlayTrigger
                    overlay={<Tooltip id={"run-proximity-analysis"}>Run Proximity Analysis</Tooltip>}>
                    {addProximityModal}
                </OverlayTrigger>
                    {runningProximityAnalysis &&
                    <p className="alert alert-warning" role="alert">
                        Currently running proximity analysis&hellip;
                        Please do not close this tab.
                    </p>
                    }
                    {(Object.keys(proximityAnalysisResults).length !== 0) && ProximityResultsDisplay()}
                </>
                }
                <br/>
                <br/>
            </div>
            }
        </div>
    );
};


Proximity.propTypes = {
    id: PropTypes.number
};

export default Proximity;
