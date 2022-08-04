import React from 'react';
import classes from './input.module.css';


const Input = React.forwardRef(({styles, input_styles, ...other}, ref) => {
    return (
        <div className={classes.input_block} style={styles}>
            <input className={classes.input} style={input_styles} type="text" ref={ref} {...other} /> 
        </div>
    );
});

export default Input;