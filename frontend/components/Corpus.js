import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
// import STYLES from "./Corpus.module.scss";
import {getCookie} from "../common";

const Corpus = ({id}) => {

    const [corpusData, setCorpusData] = useState({});
    const [allDocData, setAllDocData] = useState([]);
    const [docCheckbox, setDocCheckbox] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`/api/corpus/${id}`)
            .then(response => response.json())
            .then(data => {
                setCorpusData(data);
            });
        fetch("/api/all_documents")
            .then(response => response.json())
            .then(data => {
                setAllDocData(data);
                data.map((doc) => setDocCheckbox((values) => ({
          		    ...values,
          		    [doc.id]: corpusData.documents.includes(doc.id)
          	    })));
                setLoading(false);
            });
    }, []);

    const handleCheckBoxChange = (event) => {
        setDocCheckbox((values) => ({
            ...values,
            [event.target.id]: !docCheckbox[event.target.id]
        }));
    };

    const updateDocs = (event) => {
        event.preventDefault();
        const docList = Object.keys(docCheckbox).filter((id) => {
            return docCheckbox[id];
        }).map(id => parseInt(id));
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                id: corpusData.id,
                documents: docList
            })
        };
        fetch("api/update_corpus_docs", requestOptions)
            .then(response => response.json())
            .then(data => {
                setCorpusData(data);
            });
    };

    const allDocsList = () => {
        return (
            <form onSubmit={updateDocs}>
                <h3>Documents:</h3>
                {allDocData.map((doc, i) => (
                    <div key={i} className="custom-control custom-checkbox">
                        <input type="checkbox"
                            className="custom-control-input"
                            id={doc.id} checked={docCheckbox[doc.id]}
                            onChange={handleCheckBoxChange}/>
                        <label className="custom-control-label"
                            htmlFor={doc.id}>
                            {doc.title}, by {doc.author} {doc.year && `(${doc.year})`}</label>
                    </div>
                ))}
                <button className="btn btn-primary mt-3" type="submit">Update documents</button>
            </form>
        );
    };

    return (
        <div className="container-fluid">
            {loading
                ? <p>Currently loading Corpus...</p>
                : <div>
                    <h1>{corpusData.title}</h1>
                    <h6>Description</h6>
                    <p>{corpusData.description}</p>
                    {allDocsList()}
                </div>
            }
        </div>
    );
};

Corpus.propTypes = {
    id: PropTypes.number
};

export default Corpus;
