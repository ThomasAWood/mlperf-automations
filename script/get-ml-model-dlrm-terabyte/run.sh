#/bin/bash
if [[ ${MLC_TMP_MODEL_ADDITIONAL_NAME} ]]; then
  ln -s ${MLC_ML_MODEL_FILE} ${MLC_TMP_MODEL_ADDITIONAL_NAME}
fi
