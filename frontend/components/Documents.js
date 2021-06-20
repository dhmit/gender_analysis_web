import React, {useEffect, useState} from "react";
// import * as PropTypes from "prop-types";
// import STYLES from "./Documents.module.scss";

const Documents = () => {

    const [docData, setDocData] = useState(null);

    useEffect(() => {
        fetch("/api/all_documents")
            .then(response => response.json())
            .then(data => {
                setDocData(data);
            });
    }, []);

    return (
        <div>
            <h1>This is the Documents page.</h1>
            <p>
                This page displays all the documents stored in backend.
            </p>
            {
                docData
                    ? <div>Documents:
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
                    : <p>Currently Loading Documents...</p>
            }
        </div>
    );
};

export default Documents;
