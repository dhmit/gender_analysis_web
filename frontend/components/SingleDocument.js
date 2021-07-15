import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "../scss/SingleDocument.module.scss";
import SectionNavbar from "./SectionNavbar";
import SingleCharacter from "./SingleCharacter.js";
const SingleDocument = ({id}) => {

    const [docData, setDocData] = useState({});
    const [loading, setLoading] = useState(true);

    const tabs = ["Overview", "Characters", "Full Text"];
    const [tab, setTab] = useState(tabs[0]);

    const charList = (characters) => {
        return (
            <div className="Characters">
                {characters.length
                    ? characters.map(character => <div key={character.common_name}>
                        {SingleCharacter(character)}</div>)
                    : <div> <button className = {STYLES.button}>
                        Generate Character List
                    </button></div>
                }
            </div>
        );
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
                <div className = "document-year">
                    <b>Year of Publication: </b>{docData.year ? docData.year: "Unknown"}
                </div>
                <div className = "document-word-count">
                    <b>Word Count: </b>{docData.word_count.toLocaleString()}
                </div>
            </div>
        );
    };

    useEffect(() => {
        fetch(`/api/document/${id}`)
            .then(response => response.json())
            .then(data => {
                setDocData(data);
                setLoading(false);
            });
    }, []);


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