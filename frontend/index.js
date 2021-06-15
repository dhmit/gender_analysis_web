import React from "react";
import ReactDOM from "react-dom";
import "./scss/index.scss";
import Base from "./components/global/Base";
import ErrorNotFound from "./components/ErrorNotFound";
import ExampleId from "./components/ExampleId";

const COMPONENT_PROPS_RAW = document.getElementById("component_props").text;
const COMPONENT_NAME_RAW = document.getElementById("component_name").text;
const COMPONENT_PROPS = JSON.parse(COMPONENT_PROPS_RAW);
const COMPONENT_NAME = JSON.parse(COMPONENT_NAME_RAW);

const COMPONENTS = {
    ErrorNotFound,
    ExampleId
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || "ErrorNotFound"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);