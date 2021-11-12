import React, {useEffect, useState} from "react";
import {ButtonGroup, Dropdown, DropdownButton, Tab, Tabs} from "react-bootstrap";
import Corpus from "./Corpus";

const Analyses = () => {
    const [corporaData, setCorporaData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [corpusId, setCorpusId] = useState(1);

    useEffect(() => {
        fetch("/api/all_corpora")
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setCorporaData(data);
                setLoading(false);
            });
    }, []);

    const addCorporaDropDown = () => {
        return (
            <DropdownButton as={ButtonGroup} key='Primary' id={`dropdown-variants-Primary`} title="Corpora">
                {corporaData.map((corpus) => (
                    <Dropdown.Item key={corpus.id} eventKey={corpus.id}
                                   onSelect={() => setCorpusId(corpus.id)}>{corpus.title}</Dropdown.Item>
                ))}
            </DropdownButton>
        );
    };

    const addTabs = () => {
        return (
            <Tabs defaultActiveKey="proximity" id="analyses" className="mb-3">
                <Tab eventKey="proximity" title="Proximity">
                    <Corpus id={corpusId} key={corpusId}/>
                </Tab>
                <Tab eventKey="frequency" title="Frequency">
                </Tab>
                <Tab eventKey="dunning" title="Distinctiveness">
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
