import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "./SingleDocument.module.scss";

const SingleDocument = ({id}) => {

    const [docData, setDocData] = useState({});
    const [loading, setLoading] = useState(true);
    const [showText, setShowText] = useState(false);
    const [getCharacters, setGetCharacters] = useState(false);

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

    const SingleCharacter = (character) => {

        function renderGender(gender) {
            return gender.map((one_gender)=><span key={one_gender[0]}>{one_gender[0]}: {one_gender[1]}% </span>);
        }
        function listAliases(character) {
            return character.aliases.map((alias)=><li key={alias.name}>{alias.name}, {alias.count}</li>);
        }

        return (
            <div key={character.common_name} className = {STYLES.characterObject}>
                <div className = {STYLES.characterTitle}>
                    <span>{character.common_name ? character.common_name : "Unknown"}</span>
                    <span className = {STYLES.buttons}>
                        <span className = {STYLES.red_button}>Merge</span>
                        <span className = {STYLES.blue_button}>Delete</span>
                    </span>
                </div>
                <hr className="solid"></hr>
                <b>Full Name:</b> {character.full_name? character.full_name : "Unknown"}<br/>
                <b>Count:</b> {character.count? character.count : "Unknown"}<br/>
                <b>Gender:</b> {renderGender(character.gender)}<br/>
                <b>Aliases:</b> {listAliases(character)}<br/>
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

    const handleShowText = () => setShowText(prevShowText => !prevShowText);
    const handleGetCharacters = () => setGetCharacters(prevGetCharacters => !prevGetCharacters);

    return (
        <div className="container-fluid">
            {loading
                ? <p>Currently Loading Documents...</p>
                : <div>
                    <h1>{docData.title}</h1>
                    <p>
                        Author: {docData.author}
                        <br/>
                        Year Published {docData.year ? docData.year : "Unknown"}
                        <br/>
                        Word Count: {docData.word_count.toLocaleString()}
                    </p>
                    <div>
                        <button className="btn btn-outline-primary mb3" onClick={handleGetCharacters}>
                            {getCharacters ? "Hide Characters" : "Show Characters"}
                        </button>
                        {getCharacters && <div className={STYLES.docText}>{charList(docData.characters)}</div>}
                    </div>
                    <br/>
                    <button className="btn btn-outline-primary mb-3" onClick={handleShowText}>
                        {showText ? "Hide Full Text" : "Show Full Text"}
                    </button>
                    {showText && <p className={STYLES.docText}>{docData.text}</p>}
                </div>
            }
        </div>
    );
};


SingleDocument.propTypes = {
    id: PropTypes.number
};

export default SingleDocument;