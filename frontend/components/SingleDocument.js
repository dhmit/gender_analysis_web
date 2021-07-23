import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "../scss/SingleDocument.module.scss";
import SectionNavbar from "./SectionNavbar";
import SingleCharacter from "./SingleCharacter.js";
import {Modal} from "react-bootstrap";

const SingleDocument = ({id}) => {

    const [docData, setDocData] = useState({});
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);
    const tabs = ["Overview", "Characters", "Full Text"];
    const [tab, setTab] = useState(tabs[0]);
    const [corefParam, setCorefParam] = useState(false);

    const handleCharacterUpdate = () => {console.log("Woo!");};

    const charList = (characters) => {
        return (
            <div className="Characters">
                {characters.length
                    ? characters.map(character => <div key={character.common_name}>
                        <SingleCharacter character={character} onCharacterUpdate={handleCharacterUpdate}/></div>)
                    : <div> <button className = {STYLES.button} onClick={handleGenerateCharacter}>
                        Generate Character List: am working on it!
                    </button></div>
                }
                {getCharModal()}
            </div>
        );
    };

    const getDocData = () => {
        fetch(`/api/document/${id}`)
            .then(response => response.json())
            .then(data => {
                setDocData(data);
                setLoading(false);
            });
    };

    useEffect(() => getDocData(), []);

    // useEffect(() => { //this is what I probably should delete
    //     fetch().then(response => response.json())
    //         .then(data => {
    //             setCharData(data);
    //             setLoading(false);
    //         });
    // }, []);


    const handleGenerateCharacter = () => {
        alert("Funing is working hard to get the frontend-backend communication working!");
        getCharModal();
    };

    const getCharModal = () => {
        return (
            <>
                <button className="btn btn-primary mb-3"
                    onClick={handleShowModal}>Get Characters</button>
                <Modal show={showModal} onHide={handleCloseModal}>
                    <Modal.Header closeButton>Get Characters</Modal.Header>
                    <form onSubmit={handleSubmit}>
                        <Modal.Body>
                            <div className="row mb-3">
                                <label htmlFor="author"
                                    className="col-2 col-form-label">
                                    Would you like to calculate gender probabilities?
                                </label>
                                <div className="col">
                                    <input type="text" className="form-control"
                                        id="author" value={corefParam.author}
                                        onChange={handleCorefInputChange}/>
                                </div>
                            </div>


                        </Modal.Body>
                        <Modal.Footer>
                            <button className="btn btn-secondary"
                                onClick={handleCloseModal}>Close</button>
                            <button className="btn btn-primary"
                                type="submit">Get Characters</button>
                        </Modal.Footer>
                    </form>
                </Modal>
            </>
        );
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        handleCloseModal();
    };

    const handleCorefInputChange = (event) => {
        setCorefParam(true);
    };

    const DocumentOverview = () => {
        return (
            <div className = "document-overview">
                <div className = "document-title">
                    <b>Title: </b>{docData.title ? docData.title: "Unknown"}
                </div>
                <div className = "document-author">
                    <b>Author: </b>{docData.author ? docData.author: "Unknown"}
                </div>
                <div className = "document-publicationdate">
                    <b>Publication Year: </b>{docData.year ? docData.year: "Unknown"}
                </div>
                <div className = "document-wordcount">
                    <b>Word Count: </b>{docData.word_count ? docData.word_count: "Unknown"}
                </div>
            </div>
        );
    };


    return (
        <div className={"container-fluid"}>

            <SectionNavbar tabs = {tabs} tab = {tab} onTabChange =
                {setTab} PageTitle={docData.title}/>

            <div className = "document-content">
                { loading
                    ? <p>Currently Loading Document...</p>
                    : <div className = {STYLES.docText}>
                        {tab === "Overview" && <DocumentOverview />}
                        {tab === "Characters" && <div>{charList(docData.characters)}</div>}
                        {tab === "Full Text" && <div>{docData.text}</div>}
                    </div>
                }

            </div>
        </div>
    );
};


SingleDocument.propTypes = {
    id: PropTypes.number
};

export default SingleDocument;