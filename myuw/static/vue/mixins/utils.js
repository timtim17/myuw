
export default {
  methods: {
    encodeForMaps(s) {
      if (s) {
        s = s.replace(/ \(/g, " - ");
        s = s.replace(/[\)&]/g, "");
        s = encodeURIComponent(s);
      }
      return s;
    },
    // Phone Number Utils
    parsePhoneNumber(phNumStr) {
      let parsed = null;
      if (phNumStr) {
        let matches = phNumStr.match(/^(\+(?<country>\d+) )?(?<area>\d{3})[ -\.]?(?<exchange>\d{3})[ -\.]?(?<line>\d{4})$/);
        if (matches) {
          parsed = matches.groups;
        }
      }
      return parsed;
    },
    formatPhoneNumberDisaply(phNumStr) {
      let parsed = this.parsePhoneNumber(phNumStr);
      if (parsed) {
        return `(${parsed.area}) ${parsed.exchange}-${parsed.line}`;
      }
      return "";
    },
    formatPhoneNumberLink(phNumStr) {
      let parsed = this.parsePhoneNumber(phNumStr);
      if (parsed) {
        if (parsed.country == undefined) parsed.country = "1";
        return `+${parsed.country}-${parsed.area}-${parsed.exchange}-${parsed.line}`;
      }
      return "";
    },
    ucfirst(s) {
      return s.replace(/^([a-z])/, (c) => c.toUpperCase());
    },
  },
}