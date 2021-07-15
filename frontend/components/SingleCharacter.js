import STYLES from "./SingleCharacter.module.scss";
import {CloseRounded, DeleteRounded, MergeTypeRounded} from "@material-ui/icons";
import React from "react";

const SingleCharacter = (character) => {

    function renderGender(gender) {
        return gender.map((one_gender)=>
            <span key={one_gender[0]}>{one_gender[0]}: {one_gender[1]}% </span>);
    }

    const aliasList = (aliases) => {
        return (
            <div className={STYLES.AliasList}>
                {aliases.map((alias, i) => (
                    <div key={alias.name}>{SingleAlias(alias, i)}
                    </div>
                ))}
            </div>
        );
    };


    const SingleAlias = (alias) => {
        return (
            <span key = {alias.name} className = {STYLES.SingleAlias}>{alias.name}
                | {alias.count} <CloseRounded textSize = "inherit"/></span>
        );
    };

    return (
        <div key={character.common_name} className = {STYLES.characterObject}>
            <div className = {STYLES.characterTitle}>
                <span>{character.common_name ? character.common_name : "Unknown"}</span>
                <span className = {STYLES.buttons}>
                    <span className = {STYLES.red_button}><MergeTypeRounded /> Merge</span>
                    <span className = {STYLES.blue_button}><DeleteRounded />Delete</span>
                </span>
            </div>

            <hr className="solid" />

            <div className = {STYLES.characterMetadata}>
                <div className = {STYLES.characterStats}>
                    <b>Full Name:</b> {character.full_name? character.full_name : "Unknown"}<br/>
                    <b>Count:</b> {character.count? character.count : "Unknown"}<br/>
                    <b>Gender:</b> {renderGender(character.gender)}<br/>
                </div>
                <div className = {STYLES.characterAliases}>
                    <div className = {STYLES.aliasWordContainer}>
                        <b>Aliases:</b>
                    </div>
                    <div className = {STYLES.aliasListContainer}>
                        {aliasList(character.aliases)}
                    </div>
                </div>
            </div>
        </div>
    );
};


export default SingleCharacter;