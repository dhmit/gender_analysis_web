import React from "react";
import ReactDOM from "react-dom";
import "./scss/index.scss";
import "bootstrap/dist/css/bootstrap.min.css";
import Base from "./components/global/Base";
import ErrorNotFoundComponent from "./components/ErrorNotFoundComponent";
import ExampleId from "./components/ExampleId";
import Documents from "./components/Documents";
import SingleDocument from "./components/SingleDocument";
import Corpora from "./components/Corpora";
import Corpus from "./components/Corpus";

const COMPONENT_PROPS_RAW = document.getElementById("component_props").text;
const COMPONENT_NAME_RAW = document.getElementById("component_name").text;
const COMPONENT_PROPS = JSON.parse(COMPONENT_PROPS_RAW);
const COMPONENT_NAME = JSON.parse(COMPONENT_NAME_RAW);

const COMPONENTS = {
    ErrorNotFoundComponent,
    ExampleId,
    Documents,
    SingleDocument,
    Corpora,
    Corpus
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || "ErrorNotFoundComponent"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);
