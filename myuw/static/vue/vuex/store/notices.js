import axios from 'axios';
import {fetchBuilder, buildWith} from './model_builder';
import {strToDate} from './common';  // when uw_sws  is 2.3.8
import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))

const postProcess = (response) => {
  const notices = response.data;

  const parser = new DOMParser();
  return notices.map((notice) => {
    // Split the notice_content into notice_body and notice_title
    if (notice.notice_content.includes('&nbsp')) {
      const parts = notice.notice_content.split('&nbsp');
      notice.notice_title = parts[0];
      notice.notice_body = parts[1];
      if (notice.notice_body[0] === ';') {
        notice.notice_body = notice.notice_body.slice(1);
      }
    } else {
      const htmlDoc = parser.parseFromString(
          notice.notice_content, 'text/html',
      );
      if (htmlDoc.getElementsByClassName('notice-title')[0] !== undefined) {
        notice.notice_title = htmlDoc.getElementsByClassName(
            'notice-title',
        )[0].outerHTML;
      }
      if (htmlDoc.getElementsByClassName(
          'notice-body-with-title')[0] !== undefined) {
        notice.notice_body = htmlDoc.getElementsByClassName(
            'notice-body-with-title',
        )[0].outerHTML;
      }
    }

    // Build dates for the notices
    const dateAttr = notice.attributes.find(
        (attr) => (attr.name == 'Date'),
    );
    const startDateAttr = notice.attributes.find(
        (attr) => (attr.name == 'DisplayBegin'),
    );
    // datetime will reflect BOF
    if (startDateAttr !== undefined && startDateAttr.value !== undefined) {
      notice.startSate = dayjs.utc(startDateAttr.value);
    }
    if (dateAttr !== undefined && dateAttr.value !== undefined) {
      notice.date = dayjs.utc(dateAttr.value);
      notice.formattedDate = dateAttr.formatted_value;
    }
    // Notices will be sorted by notice.sortDate
    // some notice only has DisplayBegin date
    notice.sortDate = notice.startSate ? notice.startSate : (
      notice.date ? notice.date : null
    );
    return notice;
  });
};

const customGetters = {
  hasRegisterNotices: (state) => {
    return state.value.filter(
        (notice) => notice.location_tags.includes('checklist_no_orient') ||
          notice.location_tags.includes('checklist_orient_after') ||
          notice.location_tags.includes('checklist_iss_before') ||
          notice.location_tags.includes('checklist_iss_after') ||
          notice.location_tags.includes('checklist_measles_before') ||
          notice.location_tags.includes('checklist_measles_after') ||
          notice.location_tags.includes('checklist_orient_before'),
    ).length > 0;
  },
}

const customMutations = {
  setReadTrue(state, notice) {
    notice.is_read = true;
  },
};

const customActions = {
  setRead: ({commit, rootState}, notice) => {
    axios.put('/api/v1/notices/', {
      'notice_hashes': [notice.id_hash],
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    }).then(() => commit('setReadTrue', notice)).catch(() => {});
  },
  setReadNoUpdate: ({rootState}, notice) => {
    axios.put('/api/v1/notices/', {
      'notice_hashes': [notice.id_hash],
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    });
  },
  fetch: fetchBuilder('/api/v1/notices/', postProcess, 'json'),
};

export default buildWith(
  {customMutations, customGetters, customActions},
);
