room_mem = null;
lang_mem = null;
conf_id_mem = null;

function getValFromFormName(name) {
  var e = document.getElementsByName(name)[0];
  if (e) {
    return e.value;
  }else {
    return null;
  }
}

function getValFromFormID(id) {
  var e = document.getElementById(id);
  if (e) {
    return e.value;
  }else {
    return null;
  }
}

function getValFromRoomForm () {
  res = getValFromFormName("room");
  if (!res) {
    res = room_mem;
  } else {
    room_mem = res ;
  }
  return res;
}

function getValFromConfIDForm() {
  res = getValFromFormID("conf_id");
  if (!res) {
    res = conf_id_mem;
  } else {
    conf_id_mem = res ;
  }
  return res;
}

function getValFromLangForm () {
  res =  getValFromFormName("lang");
  if (!res) {
    res = lang_mem;
  } else {
    lang_mem = res ;
  }
  return res;
}

function initFormValues() {
  getValFromLangForm ();
  getValFromConfIDForm();
  getValFromRoomForm();
}
