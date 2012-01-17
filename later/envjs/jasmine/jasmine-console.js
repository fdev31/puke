(function() {
    if (! jasmine) {
        throw new Exception("jasmine library does not exist in global namespace!");
    }

    importPackage(java.lang);


if (!this.EnvJasmine) {
    this.EnvJasmine = {};
}


EnvJasmine.specs = [];
EnvJasmine.passedCount = 0;
EnvJasmine.failedCount = 0;
EnvJasmine.totalCount = 0;

EnvJasmine.green = "\033[32m";
EnvJasmine.red = "\033[31m";        
EnvJasmine.endColor = "\033[0m";

EnvJasmine.disableColor = false;


   

var RhinoReporter = function() {
    var results = "",
        green = EnvJasmine.green,
        red = EnvJasmine.red,
        endColor = EnvJasmine.endColor;

    if (EnvJasmine.disableColor) {
        green = "";
        red = "";
        endColor = "";
    }

    return {
        reportRunnerStarting: function(runner) {
        },

        reportRunnerResults: function(runner) {
            var passedCount = runner.results().passedCount,
                failedCount = runner.results().failedCount,
                totalCount = runner.results().totalCount;

            EnvJasmine.passedCount += passedCount;
            EnvJasmine.failedCount += failedCount;
            EnvJasmine.totalCount += totalCount;

            this.log(results);
            this.log(green + "Passed: " + passedCount + endColor);
            this.log(red + "Failed: " + failedCount + endColor);
            this.log("Total : " + totalCount + "\n");

            if (failedCount > 0) {
                System.exit(1);
            }
        },

        reportSuiteResults: function(suite) {
        },

        reportSpecStarting: function(spec) {
        },

        reportSpecResults: function(spec) {
            var i, specResults = spec.results().getItems();

            if (spec.results().passed()) {
                System.out.print(green + "." + endColor);
            } else {
                System.out.print(red + "F" + endColor);
                results += red + "\nFAILED\n";
                results += "Suite: " + this.getSuiteName(spec.suite) + "\n";
                results += "Spec : " + spec.description + "\n";
                for (i = 0; i < specResults.length; i += 1) {
                    results += specResults[i].trace + "\n";
                }
                results += endColor;
            }
        },

        log: function(str) {
            print(str);
        },

        getSuiteName: function(suite) {
            var suitePath = [];

            while (suite) {
                suitePath.push(suite.description);
                suite = suite.parentSuite;
            }

            return suitePath.join(' - ');
        }
    };
};
    // export public
    jasmine.RhinoReporter = RhinoReporter;
})();