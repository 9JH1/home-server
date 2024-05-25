function getData(endpoint) {
    return fetch(`http://127.0.0.1:8080${endpoint}`)
      .then((res) => res.text())
      .catch((error) => {});
  }