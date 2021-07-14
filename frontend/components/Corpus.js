import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
// import STYLES from "./Corpus.module.scss";
import {getCookie} from "../common";

const Corpus = ({id}) => {

    const [corpusData, setCorpusData] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`/api/corpus/${id}`)
          .then(response => response.json())
          .then(data => {
              setCorpusData(data);
              setLoading(false);
          });
    }, []);

    return (
        <div className="container-fluid">
            {loading
                ? <p>Currently loading Corpus...</p>
                : <div>
                    <h1>{corpusData.title}</h1>
                    <h6>Description</h6>
                    <p>{corpusData.description}</p>
                </div>
            }
        </div>
    );
};

Corpus.propTypes = {
    id: PropTypes.number
};

export default Corpus;
