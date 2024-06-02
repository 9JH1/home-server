function getData(endpoint) {
    return fetch(`http://192.168.68.110/${endpoint}`)
      .then((res) => res.text())
      .catch((error) => {});
  }




  /*



  laptop
    disk usage
    free space

  usb
    disk space
  */