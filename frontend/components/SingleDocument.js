import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
// import STYLES from "./SingleDocument.module.scss";

const SingleDocument = ({id}) => {

    const [docData, setDocData] = useState({});
    const [loading, setLoading] = useState(true);
    const [showText, setShowText] = useState(false);

    useEffect(() => {
        fetch(`/api/document/${id}`)
            .then(response => response.json())
            .then(data => {
                setDocData(data);
                setLoading(false);
                console.log(data);
            });
    }, []);

    const handleShowText = () => setShowText(!showText);

    return (
        <div>
            {loading
                ? <p>Currently Loading Documents...</p>
                : <div>
                    <h1>{docData.title}</h1>
                    <p>
                        Author: {docData.author}
                        <br/>
                        Word Count: {docData.word_count}
                    </p>
                    <button className="btn btn-outline-primary" onClick={handleShowText}>
                        {showText ? "Hide Full Text" : "Show Full Text"}
                    </button>
                    {showText && <p>{docData.text}</p>}
                </div>
            }
        </div>
    );
};

SingleDocument.propTypes = {
    id: PropTypes.number
};

export default SingleDocument;