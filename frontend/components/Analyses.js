import React, {useEffect, useState} from "react";
import {Dropdown, Tab, Tabs} from "react-bootstrap";
import Proximity from "./Proximity";
import Frequency from "./Frequency";
import Dunning from "./Dunning";

const Analyses = () => {
    const NO_CORPUS_SELECTED = (-1);
    const [corporaData, setCorporaData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [corpusId, setCorpusId] = useState(NO_CORPUS_SELECTED);

    useEffect(() => {
        fetch("/api/all_corpora")
            .then(response => response.json())
            .then(data => {
                setCorporaData(data);
                setLoading(false);
            });
    }, []);

    const addCorporaDropDown = () => {
        return (
            <Dropdown>
                <Dropdown.Toggle variant='dark' key='Primary' id={`dropdown-variants-Primary`}>
                    Corpora
                </Dropdown.Toggle>
                <Dropdown.Menu variant='dark'>
                    {corporaData.map((corpus) => (
                        <Dropdown.Item key={corpus.id} eventKey={corpus.id}
                                       onSelect={() => setCorpusId(corpus.id)}>{corpus.title}</Dropdown.Item>
                    ))}
                </Dropdown.Menu>
            </Dropdown>
        );
    };

    const addTabs = () => {
        return (
            <Tabs defaultActiveKey="proximity" id="analyses" className="mb-3">
                <Tab eventKey="proximity" title="Proximity">
                    <Proximity id={corpusId} key={corpusId}/>
                </Tab>
                <Tab eventKey="frequency" title="Frequency">
                    <Frequency id={corpusId} key={corpusId}/>
                </Tab>
                <Tab eventKey="dunning" title="Distinctiveness">
                    <Dunning id={corpusId} key={{corpusId}}/>
                </Tab>
            </Tabs>
        );
    };

    return (
        <div className="container-fluid">
            <p>
                This page displays all the analyses in a corpus.
            </p>
            {
                loading
                    ? <p>Currently loading Corpora&hellip;</p>
                    : <div>{addCorporaDropDown()}</div>
            }
            <br/>
            {addTabs()}
        </div>
    );
};

export default Analyses;
