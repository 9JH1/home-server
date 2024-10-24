if(oldDatabaseIndex != currentDatabaseIndex){
        uiServerFiles.innerHTML = "";
        (async () => {
          let files = JSON.parse(await getData("query_database_files/" + currentDatabaseIndex));
          for (let file of files) {
            let newEle;
            if (cend(file, ["png", "webp", "jpg", "jpeg", "gif", "pdf"])) {
              newEle = document.createElement("img");
            } else if (cend(file, ["mp4", "webm", "avi"])) {
              newEle = document.createElement("video");
              newEle.controls = "controls";
            } else {
              continue
            }
            newEle.addEventListener("click", () => {
              location.href = `${ip}${file}`;
            });
            newEle.dataset.src = `${ip}${file}`;
            uiServerFiles.append(newEle);
            observer.observe(newEle);
          }
        })();oldDatabaseIndex=currentDatabaseIndex}
      }