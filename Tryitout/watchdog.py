{"payload":{"allShortcutsEnabled":true,"fileTree":{"examples/OTA-lorawan/firmware/1.17.0/flash":{"items":[{"name":"OTA_INFO.py","path":"examples/OTA-lorawan/firmware/1.17.0/flash/OTA_INFO.py","contentType":"file"},{"name":"diff_match_patch.py","path":"examples/OTA-lorawan/firmware/1.17.0/flash/diff_match_patch.py","contentType":"file"},{"name":"loranet.py","path":"examples/OTA-lorawan/firmware/1.17.0/flash/loranet.py","contentType":"file"},{"name":"main.py","path":"examples/OTA-lorawan/firmware/1.17.0/flash/main.py","contentType":"file"},{"name":"ota.py","path":"examples/OTA-lorawan/firmware/1.17.0/flash/ota.py","contentType":"file"},{"name":"watchdog.py","path":"examples/OTA-lorawan/firmware/1.17.0/flash/watchdog.py","contentType":"file"}],"totalCount":6},"examples/OTA-lorawan/firmware/1.17.0":{"items":[{"name":"flash","path":"examples/OTA-lorawan/firmware/1.17.0/flash","contentType":"directory"}],"totalCount":1},"examples/OTA-lorawan/firmware":{"items":[{"name":"1.17.0","path":"examples/OTA-lorawan/firmware/1.17.0","contentType":"directory"},{"name":"1.17.1","path":"examples/OTA-lorawan/firmware/1.17.1","contentType":"directory"}],"totalCount":2},"examples/OTA-lorawan":{"items":[{"name":"firmware","path":"examples/OTA-lorawan/firmware","contentType":"directory"},{"name":"LoraServer.py","path":"examples/OTA-lorawan/LoraServer.py","contentType":"file"},{"name":"README.md","path":"examples/OTA-lorawan/README.md","contentType":"file"},{"name":"config.py","path":"examples/OTA-lorawan/config.py","contentType":"file"},{"name":"diff_match_patch.py","path":"examples/OTA-lorawan/diff_match_patch.py","contentType":"file"},{"name":"groupUpdater.py","path":"examples/OTA-lorawan/groupUpdater.py","contentType":"file"},{"name":"ota.py","path":"examples/OTA-lorawan/ota.py","contentType":"file"},{"name":"requirements.txt","path":"examples/OTA-lorawan/requirements.txt","contentType":"file"},{"name":"updaterService.py","path":"examples/OTA-lorawan/updaterService.py","contentType":"file"}],"totalCount":9},"examples":{"items":[{"name":"DS18X20","path":"examples/DS18X20","contentType":"directory"},{"name":"OTA-lorawan","path":"examples/OTA-lorawan","contentType":"directory"},{"name":"OTA","path":"examples/OTA","contentType":"directory"},{"name":"accelerometer_wake","path":"examples/accelerometer_wake","contentType":"directory"},{"name":"adc","path":"examples/adc","contentType":"directory"},{"name":"bluetooth","path":"examples/bluetooth","contentType":"directory"},{"name":"deepsleep","path":"examples/deepsleep","contentType":"directory"},{"name":"https","path":"examples/https","contentType":"directory"},{"name":"i2c","path":"examples/i2c","contentType":"directory"},{"name":"lopy-lopy","path":"examples/lopy-lopy","contentType":"directory"},{"name":"loraNanoGateway","path":"examples/loraNanoGateway","contentType":"directory"},{"name":"loraabp","path":"examples/loraabp","contentType":"directory"},{"name":"loramac","path":"examples/loramac","contentType":"directory"},{"name":"lorawan-nano-gateway","path":"examples/lorawan-nano-gateway","contentType":"directory"},{"name":"lorawan-regional-examples","path":"examples/lorawan-regional-examples","contentType":"directory"},{"name":"mqtt","path":"examples/mqtt","contentType":"directory"},{"name":"onlineLog","path":"examples/onlineLog","contentType":"directory"},{"name":"pytrack_pysense_accelerometer","path":"examples/pytrack_pysense_accelerometer","contentType":"directory"},{"name":"sigfoxUplink","path":"examples/sigfoxUplink","contentType":"directory"},{"name":"threading","path":"examples/threading","contentType":"directory"},{"name":"README.md","path":"examples/README.md","contentType":"file"}],"totalCount":21},"":{"items":[{"name":".github","path":".github","contentType":"directory"},{"name":"GoogleIOT","path":"GoogleIOT","contentType":"directory"},{"name":"deepsleep","path":"deepsleep","contentType":"directory"},{"name":"examples","path":"examples","contentType":"directory"},{"name":"img","path":"img","contentType":"directory"},{"name":"lib","path":"lib","contentType":"directory"},{"name":"license","path":"license","contentType":"directory"},{"name":"pycom-docker-fw-build","path":"pycom-docker-fw-build","contentType":"directory"},{"name":"pymesh","path":"pymesh","contentType":"directory"},{"name":"shields","path":"shields","contentType":"directory"},{"name":".gitignore","path":".gitignore","contentType":"file"},{"name":"Makefile","path":"Makefile","contentType":"file"},{"name":"README.md","path":"README.md","contentType":"file"}],"totalCount":13}},"fileTreeProcessingTime":19.411517,"foldersToFetch":[],"reducedMotionEnabled":"system","repo":{"id":78630626,"defaultBranch":"master","name":"pycom-libraries","ownerLogin":"pycom","currentUserCanPush":false,"isFork":false,"isEmpty":false,"createdAt":"2017-01-11T03:01:00.000-08:00","ownerAvatar":"https://avatars.githubusercontent.com/u/16415153?v=4","public":true,"private":false},"refInfo":{"name":"master","listCacheKey":"v0:1635338950.4110022","canEdit":true,"refType":"branch","currentOid":"75d0e67cb421e0576a3a9677bb0d9d81f27ebdb7"},"path":"examples/OTA-lorawan/firmware/1.17.0/flash/watchdog.py","currentUser":{"id":45674646,"login":"milesway","userEmail":"mikeli0630@gmail.com"},"blob":{"rawBlob":"#!/usr/bin/env python\n#\n# Copyright (c) 2019, Pycom Limited.\n#\n# This software is licensed under the GNU GPL version 3 or any\n# later version, with permitted additional terms. For more information\n# see the Pycom Licence v1.0 document supplied with this file, or\n# available at https://www.pycom.io/opensource/licensing\n#\n\nfrom machine import Timer\nimport _thread\n\nclass Watchdog:\n\n    def __init__(self):\n        self.failed = False\n        self.acknowledged = 0\n        self._alarm = None\n        self._lock = _thread.allocate_lock()\n\n    def enable(self, timeout = 120):\n        if self._alarm:\n            self._alarm.cancel()\n            self._alarm = None\n            \n        self._alarm = Timer.Alarm(self._check, s = timeout, periodic = True)\n\n    def _check(self, alarm):\n        with self._lock:\n            if self.acknowledged > 0:\n                self.failed = False\n                self.acknowledged = 0\n            else:\n                self.failed = True\n\n    def ack(self):\n        with self._lock:\n            self.acknowledged += 1\n\n    def update_failed(self):\n        with self._lock:\n            return self.failed\n","colorizedLines":null,"stylingDirectives":[[{"start":0,"end":21,"cssClass":"pl-c"}],[{"start":0,"end":1,"cssClass":"pl-c"}],[{"start":0,"end":36,"cssClass":"pl-c"}],[{"start":0,"end":1,"cssClass":"pl-c"}],[{"start":0,"end":62,"cssClass":"pl-c"}],[{"start":0,"end":70,"cssClass":"pl-c"}],[{"start":0,"end":65,"cssClass":"pl-c"}],[{"start":0,"end":56,"cssClass":"pl-c"}],[{"start":0,"end":1,"cssClass":"pl-c"}],[],[{"start":0,"end":4,"cssClass":"pl-k"},{"start":5,"end":12,"cssClass":"pl-s1"},{"start":13,"end":19,"cssClass":"pl-k"},{"start":20,"end":25,"cssClass":"pl-v"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":14,"cssClass":"pl-s1"}],[],[{"start":0,"end":5,"cssClass":"pl-k"},{"start":6,"end":14,"cssClass":"pl-v"}],[],[{"start":4,"end":7,"cssClass":"pl-k"},{"start":8,"end":16,"cssClass":"pl-en"},{"start":17,"end":21,"cssClass":"pl-s1"}],[{"start":8,"end":12,"cssClass":"pl-s1"},{"start":13,"end":19,"cssClass":"pl-s1"},{"start":20,"end":21,"cssClass":"pl-c1"},{"start":22,"end":27,"cssClass":"pl-c1"}],[{"start":8,"end":12,"cssClass":"pl-s1"},{"start":13,"end":25,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":28,"end":29,"cssClass":"pl-c1"}],[{"start":8,"end":12,"cssClass":"pl-s1"},{"start":13,"end":19,"cssClass":"pl-s1"},{"start":20,"end":21,"cssClass":"pl-c1"},{"start":22,"end":26,"cssClass":"pl-c1"}],[{"start":8,"end":12,"cssClass":"pl-s1"},{"start":13,"end":18,"cssClass":"pl-s1"},{"start":19,"end":20,"cssClass":"pl-c1"},{"start":21,"end":28,"cssClass":"pl-s1"},{"start":29,"end":42,"cssClass":"pl-en"}],[],[{"start":4,"end":7,"cssClass":"pl-k"},{"start":8,"end":14,"cssClass":"pl-en"},{"start":15,"end":19,"cssClass":"pl-s1"},{"start":21,"end":28,"cssClass":"pl-s1"},{"start":29,"end":30,"cssClass":"pl-c1"},{"start":31,"end":34,"cssClass":"pl-c1"}],[{"start":8,"end":10,"cssClass":"pl-k"},{"start":11,"end":15,"cssClass":"pl-s1"},{"start":16,"end":22,"cssClass":"pl-s1"}],[{"start":12,"end":16,"cssClass":"pl-s1"},{"start":17,"end":23,"cssClass":"pl-s1"},{"start":24,"end":30,"cssClass":"pl-en"}],[{"start":12,"end":16,"cssClass":"pl-s1"},{"start":17,"end":23,"cssClass":"pl-s1"},{"start":24,"end":25,"cssClass":"pl-c1"},{"start":26,"end":30,"cssClass":"pl-c1"}],[],[{"start":8,"end":12,"cssClass":"pl-s1"},{"start":13,"end":19,"cssClass":"pl-s1"},{"start":20,"end":21,"cssClass":"pl-c1"},{"start":22,"end":27,"cssClass":"pl-v"},{"start":28,"end":33,"cssClass":"pl-v"},{"start":34,"end":38,"cssClass":"pl-s1"},{"start":39,"end":45,"cssClass":"pl-s1"},{"start":47,"end":48,"cssClass":"pl-s1"},{"start":49,"end":50,"cssClass":"pl-c1"},{"start":51,"end":58,"cssClass":"pl-s1"},{"start":60,"end":68,"cssClass":"pl-s1"},{"start":69,"end":70,"cssClass":"pl-c1"},{"start":71,"end":75,"cssClass":"pl-c1"}],[],[{"start":4,"end":7,"cssClass":"pl-k"},{"start":8,"end":14,"cssClass":"pl-en"},{"start":15,"end":19,"cssClass":"pl-s1"},{"start":21,"end":26,"cssClass":"pl-s1"}],[{"start":8,"end":12,"cssClass":"pl-k"},{"start":13,"end":17,"cssClass":"pl-s1"},{"start":18,"end":23,"cssClass":"pl-s1"}],[{"start":12,"end":14,"cssClass":"pl-k"},{"start":15,"end":19,"cssClass":"pl-s1"},{"start":20,"end":32,"cssClass":"pl-s1"},{"start":33,"end":34,"cssClass":"pl-c1"},{"start":35,"end":36,"cssClass":"pl-c1"}],[{"start":16,"end":20,"cssClass":"pl-s1"},{"start":21,"end":27,"cssClass":"pl-s1"},{"start":28,"end":29,"cssClass":"pl-c1"},{"start":30,"end":35,"cssClass":"pl-c1"}],[{"start":16,"end":20,"cssClass":"pl-s1"},{"start":21,"end":33,"cssClass":"pl-s1"},{"start":34,"end":35,"cssClass":"pl-c1"},{"start":36,"end":37,"cssClass":"pl-c1"}],[{"start":12,"end":16,"cssClass":"pl-k"}],[{"start":16,"end":20,"cssClass":"pl-s1"},{"start":21,"end":27,"cssClass":"pl-s1"},{"start":28,"end":29,"cssClass":"pl-c1"},{"start":30,"end":34,"cssClass":"pl-c1"}],[],[{"start":4,"end":7,"cssClass":"pl-k"},{"start":8,"end":11,"cssClass":"pl-en"},{"start":12,"end":16,"cssClass":"pl-s1"}],[{"start":8,"end":12,"cssClass":"pl-k"},{"start":13,"end":17,"cssClass":"pl-s1"},{"start":18,"end":23,"cssClass":"pl-s1"}],[{"start":12,"end":16,"cssClass":"pl-s1"},{"start":17,"end":29,"cssClass":"pl-s1"},{"start":30,"end":32,"cssClass":"pl-c1"},{"start":33,"end":34,"cssClass":"pl-c1"}],[],[{"start":4,"end":7,"cssClass":"pl-k"},{"start":8,"end":21,"cssClass":"pl-en"},{"start":22,"end":26,"cssClass":"pl-s1"}],[{"start":8,"end":12,"cssClass":"pl-k"},{"start":13,"end":17,"cssClass":"pl-s1"},{"start":18,"end":23,"cssClass":"pl-s1"}],[{"start":12,"end":18,"cssClass":"pl-k"},{"start":19,"end":23,"cssClass":"pl-s1"},{"start":24,"end":30,"cssClass":"pl-s1"}]],"csv":null,"csvError":null,"dependabotInfo":{"showConfigurationBanner":false,"configFilePath":null,"networkDependabotPath":"/pycom/pycom-libraries/network/updates","dismissConfigurationNoticePath":"/settings/dismiss-notice/dependabot_configuration_notice","configurationNoticeDismissed":false,"repoAlertsPath":"/pycom/pycom-libraries/security/dependabot","repoSecurityAndAnalysisPath":"/pycom/pycom-libraries/settings/security_analysis","repoOwnerIsOrg":true,"currentUserCanAdminRepo":false},"displayName":"watchdog.py","displayUrl":"https://github.com/pycom/pycom-libraries/blob/master/examples/OTA-lorawan/firmware/1.17.0/flash/watchdog.py?raw=true","headerInfo":{"blobSize":"1.11 KB","deleteInfo":{"deletePath":"https://github.com/pycom/pycom-libraries/delete/master/examples/OTA-lorawan/firmware/1.17.0/flash/watchdog.py","deleteTooltip":"Fork this repository and delete the file"},"editInfo":{"editTooltip":"Fork this repository and edit the file"},"ghDesktopPath":"https://desktop.github.com","gitLfsPath":null,"onBranch":true,"shortPath":"299c736","siteNavLoginPath":"/login?return_to=https%3A%2F%2Fgithub.com%2Fpycom%2Fpycom-libraries%2Fblob%2Fmaster%2Fexamples%2FOTA-lorawan%2Ffirmware%2F1.17.0%2Fflash%2Fwatchdog.py","isCSV":false,"isRichtext":false,"toc":null,"lineInfo":{"truncatedLoc":"43","truncatedSloc":"35"},"mode":"file"},"image":false,"isCodeownersFile":null,"isValidLegacyIssueTemplate":false,"issueTemplateHelpUrl":"https://docs.github.com/articles/about-issue-and-pull-request-templates","issueTemplate":null,"discussionTemplate":null,"language":"Python","large":false,"loggedIn":true,"newDiscussionPath":"/pycom/pycom-libraries/discussions/new","newIssuePath":"/pycom/pycom-libraries/issues/new","planSupportInfo":{"repoIsFork":null,"repoOwnedByCurrentUser":null,"requestFullPath":"/pycom/pycom-libraries/blob/master/examples/OTA-lorawan/firmware/1.17.0/flash/watchdog.py","showFreeOrgGatedFeatureMessage":null,"showPlanSupportBanner":null,"upgradeDataAttributes":null,"upgradePath":null},"publishBannersInfo":{"dismissActionNoticePath":"/settings/dismiss-notice/publish_action_from_dockerfile","dismissStackNoticePath":"/settings/dismiss-notice/publish_stack_from_file","releasePath":"/pycom/pycom-libraries/releases/new?marketplace=true","showPublishActionBanner":false,"showPublishStackBanner":false},"renderImageOrRaw":false,"richText":null,"renderedFileInfo":null,"tabSize":8,"topBannersInfo":{"overridingGlobalFundingFile":false,"globalPreferredFundingPath":null,"repoOwner":"pycom","repoName":"pycom-libraries","showInvalidCitationWarning":false,"citationHelpUrl":"https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files","showDependabotConfigurationBanner":false,"actionsOnboardingTip":null},"truncated":false,"viewable":true,"workflowRedirectUrl":null,"symbols":{"timedOut":false,"notAnalyzed":false,"symbols":[{"name":"Watchdog","kind":"class","identStart":371,"identEnd":379,"extentStart":365,"extentEnd":1137,"fullyQualifiedName":"Watchdog","identUtf16":{"start":{"lineNumber":13,"utf16Col":6},"end":{"lineNumber":13,"utf16Col":14}},"extentUtf16":{"start":{"lineNumber":13,"utf16Col":0},"end":{"lineNumber":42,"utf16Col":30}}},{"name":"__init__","kind":"function","identStart":390,"identEnd":398,"extentStart":386,"extentEnd":535,"fullyQualifiedName":"Watchdog.__init__","identUtf16":{"start":{"lineNumber":15,"utf16Col":8},"end":{"lineNumber":15,"utf16Col":16}},"extentUtf16":{"start":{"lineNumber":15,"utf16Col":4},"end":{"lineNumber":19,"utf16Col":44}}},{"name":"enable","kind":"function","identStart":545,"identEnd":551,"extentStart":541,"extentEnd":751,"fullyQualifiedName":"Watchdog.enable","identUtf16":{"start":{"lineNumber":21,"utf16Col":8},"end":{"lineNumber":21,"utf16Col":14}},"extentUtf16":{"start":{"lineNumber":21,"utf16Col":4},"end":{"lineNumber":26,"utf16Col":76}}},{"name":"_check","kind":"function","identStart":761,"identEnd":767,"extentStart":757,"extentEnd":971,"fullyQualifiedName":"Watchdog._check","identUtf16":{"start":{"lineNumber":28,"utf16Col":8},"end":{"lineNumber":28,"utf16Col":14}},"extentUtf16":{"start":{"lineNumber":28,"utf16Col":4},"end":{"lineNumber":34,"utf16Col":34}}},{"name":"ack","kind":"function","identStart":981,"identEnd":984,"extentStart":977,"extentEnd":1051,"fullyQualifiedName":"Watchdog.ack","identUtf16":{"start":{"lineNumber":36,"utf16Col":8},"end":{"lineNumber":36,"utf16Col":11}},"extentUtf16":{"start":{"lineNumber":36,"utf16Col":4},"end":{"lineNumber":38,"utf16Col":34}}},{"name":"update_failed","kind":"function","identStart":1061,"identEnd":1074,"extentStart":1057,"extentEnd":1137,"fullyQualifiedName":"Watchdog.update_failed","identUtf16":{"start":{"lineNumber":40,"utf16Col":8},"end":{"lineNumber":40,"utf16Col":21}},"extentUtf16":{"start":{"lineNumber":40,"utf16Col":4},"end":{"lineNumber":42,"utf16Col":30}}}]}},"csrf_tokens":{"/pycom/pycom-libraries/branches":{"post":"XCjCJ92GxY76tO4urynS3C_h7RLys6J9Q2_AXTHlg-HZ5KxETD9NyjUTJwtpR0UXF2BRib4f8Q9aVas0xFPkng"}}},"title":"pycom-libraries/watchdog.py at master · pycom/pycom-libraries","locale":"en"}