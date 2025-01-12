<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h2>
    </template>
    <template v-else #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Seattle Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h2>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        For application status, contact the Office of the University Registrar
      </h3>
      <div class="container">
        <div class="row">
          <div class="col">Email</div>
          <div class="col"><a v-out="'Contact Registrar Office'"
                   href="mailto:regoff@uw.edu">regoff@uw.edu</a></div>
        </div>
        <div class="row">
          <div class="col">Phone</div>
          <div class="col">(206) 543-4000</div>
        </div>
        <div class="row">
          <div class="col">Location</div>
          <div class="col">225 Schmitz Hall</div>
        </div>
      </div>

      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        Registration for Returning Student
      </h3>
      <p>
        You must confirm your intent to attend prior to being able to register.
      </p>
      <p>
        You may register during the Registration Period II of your
        quarter of readmittance. Check dates in the
        <a href="http://www.washington.edu/students/reg/calendar.html"
        >Academic calendar</a>.
      </p>

      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        Resources for Seattle Applicants
      </h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a
            v-out="'Student Financial Aid'"
            href="https://www.washington.edu/financialaid/"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'Student Guide'"
             href="http://www.washington.edu/students/"
          >
            Check out the Student guide for academics, student life, and more
          </a>
        </li>
        <li class="mb-1">
          <a
            href="http://www.washington.edu/students/reg/calendar.html"
          >
            View the UW Academic calendars
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <uw-link-button class="my-4"
        href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp"
      >
        View your {{ applicantData.type }} application status
      </uw-link-button>

      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        Resources for Seattle Applicants
      </h3>
      <h4 class="h6">
        ADMISSIONS
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li v-if="applicantData.is_freshman" class="mb-1">
          <a
            href="https://admit.washington.edu/apply/dates-deadlines/"
          >
            Key dates &amp; deadlines for freshmen
          </a>
        </li>
        <li v-if="applicantData.is_transfer" class="mb-1">
          <a
            href="https://admit.washington.edu/apply/dates-deadlines/#transfer"
          >
            Key dates &amp; deadlines for Transfer
          </a>
        </li>
        <li v-if="applicantData.if_post_bac" class="mb-1">
          <a
            href="https://admit.washington.edu/apply/dates-deadlines/#postbac"
          >
            Key dates &amp; deadlines for Postbaccalaureate
          </a>
        </li>
      </ul>

      <h4 class="h6">
        FINANCES
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a
            href="https://www.washington.edu/financialaid/"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li class="mb-1">
          <a
            href="https://admit.washington.edu/costs/coa/"
          >
            Refer to total cost of attendance for financial planning
          </a>
        </li>
      </ul>

      <h4 class="h6">
        STUDENT LIFE
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a href="http://admit.washington.edu/Visit">
            Plan your visit: Seattle campus tours
          </a>
        </li>
        <li class="mb-1">
          <a href="https://hfs.uw.edu/Live">
            Learn about campus-living
          </a>
        </li>
        <li class="mb-1">
          <a
            href="http://hr.uw.edu/dso/services/matriculated-students/"
          >
            Check out student services: Disability Resources
          </a>
        </li>
      </ul>
      <h4 class="h6">
        IF ADMITTED
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a
            href="http://www.washington.edu/newhuskies/must-do/"
          >
            Next steps for Admitted students
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'Accept admission offer'"
             href="http://www.washington.edu/newhuskies/must-do/#accept/"
          >
            Accept the admission offer and pay the New Student Enrollment
            &amp; Orientation Fee
          </a>
        </li>
        <li v-if="applicantData.is_international" class="mb-1">
          <a v-out="'Intl student checklist'"
             href="https://iss.washington.edu/new-students/"
          >
            View the Int’l student checklist from International Student
            Services (ISS)
          </a>
        </li>
        <li class="mb-1">
          <a
            href="http://fyp.washington.edu/getting-started-at-the-university-of-washington/"
          >
            Register for an Advising &amp; Orientation session
          </a>
        </li>
        <li class="mb-1">
          <a
            href="http://www.washington.edu/uaa/advising/academic-planning/majors-and-minors/list-of-undergraduate-majors/"
          >
            View undergraduate Majors
          </a>
        </li>
        <li class="mb-1">
          <a href="http://fyp.washington.edu/">
            Learn about the First Year Programs
          </a>
        </li>
        <li class="mb-1">
          <a href="http://www.washington.edu/students/">
            Check out the Student guide
          </a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';
import LinkButton from '../../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link-button': LinkButton,
  },
  props: {
    applicantData: {
      type: [Object, Boolean],
      default: false,
    },
    isReady: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
