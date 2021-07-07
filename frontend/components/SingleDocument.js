import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import STYLES from "./SingleDocument.module.scss";

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
            });
    }, []);

    const handleShowText = () => setShowText(prevShowText => !prevShowText);

    const frequencyModule = () => {
        return (
            <form>
                <div className="form-check">
                    <input className="form-check-input" type="checkbox" value="" id="female"/>
                    <label className="form-check-label" htmlFor="female">
                        Female
                    </label>
                </div>
                <div className="form-check">
                    <input className="form-check-input" type="checkbox" value="" id="male"/>
                    <label className="form-check-label" htmlFor="male">
                        Male
                    </label>
                </div>
            </form>
        );
    };

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
                    <h3>Analyses</h3>
                    <h5>Frequency</h5>
                    {frequencyModule()}
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