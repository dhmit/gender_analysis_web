import React, {useEffect, useState} from "react";
// import * as PropTypes from "prop-types";
// import STYLES from "./Documents.module.scss";

const Documents = () => {

    const [docData, setDocData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [addingDoc, setAddingDoc] = useState(false);

    useEffect(() => {
        fetch("/api/all_documents")
            .then(response => response.json())
            .then(data => {
                setDocData(data);
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <h1>This is the Documents page.</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>
            {
                loading
                    ? <p>Currently Loading Documents...</p>
                    : <div>Documents:
                        {docData.map((doc, i) => {
                            return (<>
                                <p>Document {i}</p>
                                <ul key={i}>
                                    {Object.keys(doc).map((key, i) => {
                                        return (
                                            <li key={i}>{key}: {doc[key]}</li>
                                        );
                                    })}
                                </ul>
                            </>
                            );
                        })}
                    </div>
            }
        </div>
    );
};

export default Documents;
