import React from "react";
import ReactDOM from "react-dom";
import "./scss/index.scss";
import Base from "./components/global/Base";
import ErrorNotFound from "./components/ErrorNotFound";
import ExampleId from "./components/ExampleId";

const APP_DATA_RAW = document.getElementById("app_data").text;
const APP_COMPONENT_RAW = document.getElementById("app_component").text;
const APP_DATA = JSON.parse(APP_DATA_RAW);
const APP_COMPONENT = JSON.parse(APP_COMPONENT_RAW);

const COMPONENTS = {
    ErrorNotFound,
    ExampleId
};

const PreselectedComponent = COMPONENTS[APP_COMPONENT || "ErrorNotFound"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...APP_DATA}/>
    </Base>,
    document.getElementById("app_root")
);