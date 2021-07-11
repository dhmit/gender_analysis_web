import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "./SingleDocument.module.scss";

const SingleDocument = ({id}) => {

    const [docData, setDocData] = useState({});
    const [loading, setLoading] = useState(true);
    const [showText, setShowText] = useState(false);
    const [getCharacters, setGetCharacters] = useState(false);

    function renderGender(gender) {
        return gender.map((one_gender)=><span key={one_gender[0]}><b>{one_gender[0]}: {one_gender[1]}%   </b></span>);
    }
    function listAliases(character) {
        return character.aliases.map((alias)=><li key={alias.name}>{alias.name}, {alias.count}</li>);
    }

    function listCharacters() {
        return docData.characters.map((char) => <p key={char.common_name}><h3>{char.common_name}</h3>
            Full Name: {char.full_name}<br/>
            Count: {char.count}<br/>
            Gender: {renderGender(char.gender)}<br/>
            Aliases: {listAliases(char)}
        </p>);
    }


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
                        Year Published {docData.year ? docData : "Unknown"}
                        <br/>
                        Word Count: {docData.word_count.toLocaleString()}
                    </p>
                    <p>
                        <button className="btn btn-outline-primary mb3" onClick={handleGetCharacters}>
                        {getCharacters ? "Hide Characters" : "Show Characters"}
                        </button>
                        {getCharacters && <p className={STYLES.docText}>{listCharacters()}</p>}
                    </p>
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