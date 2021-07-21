import STYLES from "../scss/SingleCharacter.module.scss";
import {CloseRounded, DeleteRounded, MergeTypeRounded} from "@material-ui/icons";

import React, {useState} from "react";
import {getCookie} from "../common";


const SingleCharacter = (character) => {

//    const [aliasState, setAliasState] = useState(character.aliases);

    const handleRemoveAlias = (alias) => {
        const csrftoken = getCookie("csrftoken");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                alias_id: alias.name,
                character_id: character.common_name,
            })
        };
        console.log({alias, character});
        fetch("/api/remove_alias", requestOptions)
            .then(response => response.json());
            // .then(() => {
            //     setAliasState((previousState) =>
            //         previousState.filter((previousAlias) => previousAlias.name !== alias.name)
            //     );
            // });
    };

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
            <button key = {alias.name} className = {STYLES.SingleAlias}
                onClick = {() => handleRemoveAlias(alias)}>
                {alias.name} ({alias.count})
                <CloseRounded /></button>
        );
    };

    return (
        <div key={character.common_name} className = {STYLES.characterObject}>
            <div className = {STYLES.characterTitle}>
                <span>{character.common_name ? character.common_name : "Unknown"}</span>
                <span className = {STYLES.buttons}>
                    <button className = {STYLES.blue_button}><MergeTypeRounded />Merge</button>
                    <button className = {STYLES.red_button}><DeleteRounded />Delete</button>
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