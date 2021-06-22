import React, {useEffect, useState} from "react";
// import * as PropTypes from "prop-types";
// import STYLES from "./Documents.module.scss";


const Documents = () => {

    const [docData, setDocData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("/api/all_documents")
            .then(response => response.json())
            .then(data => {
                setDocData(data);
                setLoading(false);
            });
    }, []);

    const docInfo = (doc) => {
        return (
            <ul>
                {Object.keys(doc).map((attribute, i) => (
                    <li key={i}>{key}: {doc[key]}</li>
                ))}
            </ul>
        );
    };

    const docList = () => {
        return (
            <ul>
                {docData.map((doc, i) => (
                    <li key={i}> {docInfo(doc)} </li>
                ))}
            </ul>
        );
    };

    return (
        <div>
            <h1>This is the Documents page.</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>
            {
                loading
                    ? <p>Currently Loading Documents...</p>
                    : <div>
                        Documents:
                        {docList()}
                    </div>
            }
        </div>
    );
};

export default Documents;
