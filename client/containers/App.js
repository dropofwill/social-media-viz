import React, { PropTypes } from 'react';

const App = ({ state }) => (
  <div>{state}</div>
);

App.propTypes = {
  state: PropTypes.number.isRequired,
};

export default App;
