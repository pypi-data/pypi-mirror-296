$$HREPR = {
    scriptStatus: {},
    counters: {},
    fromHTML(html) {
        const node = document.createElement("div");
        node.innerHTML = html;
        return node.childNodes[0];
    },
    prepare(node_id) {
        const self = document.getElementById(node_id);
        let resolve = null;
        self.__object = new Promise((rs, rj) => { resolve = rs });
        self.__object.__resolve = resolve;
        return self;
    },
    swap(orig, repl) {
        if (repl?.getElement) {
            repl = repl.getElement();
        }
        if (!(repl instanceof HTMLElement)) {
            repl = window.$$REPRESENT?.(repl);
        }
        if (repl instanceof HTMLElement) {
            repl.__object = orig.__object;
            for (let attr of orig.attributes) {
                if (attr.name === "class") {
                    repl.classList.add(...orig.classList);
                }
                else {
                    repl.setAttribute(attr.name, attr.value);
                }
            }
            orig.replaceWith(repl);
        }
        else {
            orig.remove();
        }
    },
    isFunc(x) {
        let hasprop = prop => Object.getOwnPropertyNames(x).includes(prop);
        return (hasprop("arguments") || !hasprop("prototype"));
    },
    trycb(cb, ecb, sel) {
        try {
            cb();
        }
        catch (error) {
            if (!ecb?.(error, sel)) {
                throw error;
            };
        }
    },
    run(scripts, sel, cb, ecb = null) {
        ecb = ecb || window.$$ERROR;
        if (scripts.length == 0) {
            $$HREPR.trycb(cb, ecb, sel);
            return;
        }
        const counter = {count: scripts.length, cb, ecb, sel};
        for (let script of scripts) {
            let counters = (this.counters[script] ||= []);
            counters.push(counter);
            let status = this.scriptStatus[script];
            if (status === undefined) {
                this.scriptStatus[script] = false;
                let scriptTag = document.createElement("script");
                scriptTag.src = script;
                scriptTag.onerror = (err) => {
                    err = Error(`Could not load script: ${script}`);
                    err.stack = null;
                    $$HREPR.scriptStatus[script] = err;
                    $$HREPR.triggerScript(script, err);
                };
                scriptTag.onload = () => {
                    $$HREPR.scriptStatus[script] = true;
                    $$HREPR.triggerScript(script);
                };
                document.head.appendChild(scriptTag);    
            }
            else if (status instanceof Error) {
                ecb?.(status, sel);
            }
            else if (status) {
                $$HREPR.triggerScript(script);
            }
        }
    },
    triggerScript(script, error = null) {
        for (let counter of this.counters[script] || []) {
            counter.count--;
            if (!counter.count) {
                if (error) {
                    counter.ecb?.(error, counter.sel);
                }
                else {
                    $$HREPR.trycb(counter.cb, counter.ecb, counter.sel);
                }
            }
        }
    },
    ucall(obj, sym, ...arglist) {
        if (sym) {
            return $$HREPR.isFunc(obj[sym]) ? obj[sym](...arglist) : new obj[sym](...arglist);
        }
        else {
            return $$HREPR.isFunc(obj) ? obj(...arglist) : new obj(...arglist);
        }
    },
}
