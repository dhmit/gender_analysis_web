import * as PropTypes from "prop-types";
import STYLES from "./SectionNavbar.module.scss";
import React from "react";


const SectionNavbar = ({tabs, tab, onTabChange, PageTitle}) => {
    return (
        <div className = "section-navbar">
            <div className = {STYLES.Title}>{PageTitle}</div>

            <div className = "navbar-buttons">
                {
                    tabs.map(tab_name => (
                        <button className = {tab_name === tab
                            ? STYLES.ActiveTabButton
                            : STYLES.InactiveTabButton
                        }
                        key={tab_name} onClick={() => onTabChange(tab_name)}>{tab_name}</button>
                    ))
                }
                <hr className = "solid" />
            </div>
        </div>
    );
};

SectionNavbar.propTypes = {
    tabs: PropTypes.arrayOf(PropTypes.string),
    tab: PropTypes.string,
    onTabChange: PropTypes.func,
    PageTitle: PropTypes.string
};

SectionNavbar.defaultProps = {
    tabs: [],
    tab: "",
    onTabChange: () => {},
    PageTitle: "GATK"
};

export default SectionNavbar;