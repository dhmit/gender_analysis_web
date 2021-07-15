import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "./SingleDocument.module.scss";
import {MergeTypeRounded} from "@material-ui/icons";
import {DeleteRounded} from "@material-ui/icons";
import {CloseRounded} from "@material-ui/icons";
import {PeopleAltRounded} from "@material-ui/icons";
import {getCookie} from "../common";
import {Modal} from "react-bootstrap";
import SectionNavbar from './SectionNavbar';

const SingleDocument = ({id}) => {

    const [docData, setDocData] = useState({});
    const [loading, setLoading] = useState(true);
    const [showText, setShowText] = useState(false);
    const [getCharacters, setGetCharacters] = useState(false);

    const tabs = ['Overview', 'Characters', 'Full Text'];
    const [tab, setTab] = useState(tabs[0]);

    const charList = (characters) => {
        return (
            <div className="Characters">
                {characters.map((character, i) => (
                    <div key={character.common_name}>{SingleCharacter(character, i)}
                    </div>
                ))}
            </div>
        );
    };

    const aliasList = (aliases) => {
        return (
            <div className={STYLES.AliasList}>
                {aliases.map((alias, i) => (
                    <div key={alias.name}>{SingleAlias(alias, i)}
                    </div>
                ))}
            </div>
        );
    };

    const SingleCharacter = (character) => {


        function renderGender(gender) {
            return gender.map((one_gender)=>
                <span key={one_gender[0]}>{one_gender[0]}: {one_gender[1]}% </span>);
        }

        return (
            <div key={character.common_name} className = {STYLES.characterObject}>
                <div className = {STYLES.characterTitle}>
                    <span>{character.common_name ? character.common_name : "Unknown"}</span>
                    <span className = {STYLES.buttons}>
                        <span className = {STYLES.red_button}><MergeTypeRounded /> Merge</span>
                        <span className = {STYLES.blue_button}><DeleteRounded />Delete</span>
                    </span>
                </div>

                <hr className="solid" />

                <div className = {STYLES.characterMetadata}>
                    <div className = {STYLES.characterStats}>
                        <b>Full Name:</b> {character.full_name? character.full_name : "Unknown"}<br/>
                        <b>Count:</b> {character.count? character.count : "Unknown"}<br/>
                        <b>Gender:</b> {renderGender(character.gender)}<br/>
                    </div>
                    <div className = {STYLES.characterAliases}>
                        <div className = {STYLES.aliasWordContainer}>
                            <b>Aliases:</b>
                        </div>
                        <div className = {STYLES.aliasListContainer}>
                            {aliasList(character.aliases)}
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    const SingleAlias = (alias) => {
        return (
            <span key = {alias.name} className = {STYLES.SingleAlias}>{alias.name} | {alias.count} <CloseRounded textSize = "inherit"/></span>
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

            <SectionNavbar tabs = {tabs} tab = {tab} onTabChange = {setTab} PageTitle={docData.title}/>

            <div className = "document-content">
                { loading
                    ? <p>Currently Loading Document...</p>
                    : <div className = {STYLES.docText}>
                        {tab === 'Overview' && "Overview Goes Here"}
                        {tab === 'Characters' && <div>{charList(docData.characters)}</div>}
                        {tab === 'Full Text' && <div>{docData.text}</div>}
                    </div>
                }

            </div>
        </div>
    );


    // return (
    //     <div className="container-fluid">
    //         {loading
    //             ? <p>Currently Loading Documents...</p>
    //             : <div>
    //                 <h1>{docData.title}</h1>
    //                 <p>
    //                     Author: {docData.author}
    //                     <br/>
    //                     Year Published {docData.year ? docData.year : "Unknown"}
    //                     <br/>
    //                     Word Count: {docData.word_count.toLocaleString()}
    //                 </p>
    //                 <div>
    //                     <button className="btn btn-outline-primary mb3" onClick={handleGetCharacters}>
    //                         {getCharacters ? "Hide Characters" : "Show Characters"}
    //                     </button>
    //                     {getCharacters && <div className={STYLES.docText}>{charList(docData.characters)}</div>}
    //                 </div>
    //                 <br/>
    //                 <button className="btn btn-outline-primary mb-3" onClick={handleShowText}>
    //                     {showText ? "Hide Full Text" : "Show Full Text"}
    //                 </button>
    //                 {showText && <p className={STYLES.docText}>{docData.text}</p>}
    //             </div>
    //         }
    //     </div>
    // );
};


SingleDocument.propTypes = {
    id: PropTypes.number
};

export default SingleDocument;