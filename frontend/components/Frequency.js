import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import {Alert, Form} from "react-bootstrap";
import {getCookie} from "../common";


const Frequency = ({id}) => {
    const [genders, setGenders] = useState([]);
    const [containsGender, setContainsGender] = useState({});
    const [gendersLoading, setGendersLoading] = useState(true);
    const [selectedGenders, setSelectedGenders] = useState([]);
    const [runningFrequencyAnalysis, setRunningFrequencyAnalysis] = useState(false);
    const [frequencyAnalysisResults, setFrequencyAnalysisResults] = useState({});

    useEffect(() => {
        fetch("/api/all_genders")
            .then(response => response.json())
            .then(data => {
                setGenders(data);
                setGendersLoading(false);
            });
    }, []);

    const handleCheckBoxChange = (event) => {
        setContainsGender((values) => ({
            ...values,
            [event.target.id]: true
        }));
        console.log(containsGender);
    };

    const handleFrequencyAnalysisSubmit = (event) => {
        event.preventDefault();
        const gendersList = Object.keys(containsGender).filter((id) => {
            return containsGender[id];
        });
        console.log(gendersList);
        setRunningFrequencyAnalysis(true);
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                corpus_id: id,
                gender_ids: gendersList
            })
        };
        fetch("/api/frequency", requestOptions)
            .then(response => response.json())
            .then(data => {
                setFrequencyAnalysisResults(data.results);
                setRunningFrequencyAnalysis(false);
                console.log(data.results);
            });
    };

    const corpusNotSelectedWarning = () => {
        return (<Alert key='select-corpus-id' variant='danger'>
            Please select a corpus.
        </Alert>);
    };

    const updateGendersSelection = () => {
        return (
            (id === -1) ? corpusNotSelectedWarning() :
            <Form onSubmit={handleFrequencyAnalysisSubmit}>
                {genders.map((gender) => (
                    <div key={`inline-${gender.label}`} className="mb-3">
                        <Form.Check key={`key-${gender.label}`} inline label={gender.label}
                                    id={gender.id} checked={containsGender[gender.id]} onChange={handleCheckBoxChange}/>
                    </div>
                ))}
                <button className="btn btn-danger btn-sm" type="submit">
                    Run Frequency Analysis
                </button>
            </Form>
        );
    };


    return (
        <div>{updateGendersSelection()}</div>
    );
};


Frequency.propTypes = {
    id: PropTypes.number
};

export default Frequency;
