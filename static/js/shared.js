function getData(endpoint) {
    return fetch(`http://198.168.68.110/${endpoint}`)
      .then((res) => res.text())
      .catch((error) => {});
  }