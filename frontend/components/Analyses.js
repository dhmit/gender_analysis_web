import React, {useEffect, useState} from "react";
import {ButtonGroup, Dropdown, DropdownButton} from "react-bootstrap";

const Analyses = () => {
    const [corporaData, setCorporaData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [corpusId, setCorpusId] = useState(undefined);

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
        </div>
    );
};

export default Analyses;
