import { g as Me, w as E, c as Le } from "./Index-D21tLoTw.js";
const he = window.ms_globals.React, Ae = window.ms_globals.React.forwardRef, Ye = window.ms_globals.React.useRef, pe = window.ms_globals.React.useEffect, xe = window.ms_globals.React.useMemo, Fe = window.ms_globals.React.useState, ee = window.ms_globals.ReactDOM.createPortal, Ne = window.ms_globals.antdCssinjs.StyleProvider, Te = window.ms_globals.antd.ConfigProvider, H = window.ms_globals.antd.theme, ye = window.ms_globals.dayjs;
var ge = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var je = he, He = Symbol.for("react.element"), Ke = Symbol.for("react.fragment"), Ue = Object.prototype.hasOwnProperty, Be = je.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, We = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function we(e, t, r) {
  var n, i = {}, o = null, s = null;
  r !== void 0 && (o = "" + r), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) Ue.call(t, n) && !We.hasOwnProperty(n) && (i[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) i[n] === void 0 && (i[n] = t[n]);
  return {
    $$typeof: He,
    type: e,
    key: o,
    ref: s,
    props: i,
    _owner: Be.current
  };
}
x.Fragment = Ke;
x.jsx = we;
x.jsxs = we;
ge.exports = x;
var z = ge.exports;
const {
  SvelteComponent: Ge,
  assign: te,
  binding_callbacks: re,
  check_outros: qe,
  component_subscribe: ne,
  compute_slots: Ze,
  create_slot: Je,
  detach: I,
  element: be,
  empty: Qe,
  exclude_internal_props: oe,
  get_all_dirty_from_scope: Xe,
  get_slot_changes: Ve,
  group_outros: $e,
  init: et,
  insert: O,
  safe_not_equal: tt,
  set_custom_element_data: Pe,
  space: rt,
  transition_in: R,
  transition_out: W,
  update_slot_base: nt
} = window.__gradio__svelte__internal, {
  beforeUpdate: ot,
  getContext: it,
  onDestroy: st,
  setContext: lt
} = window.__gradio__svelte__internal;
function ie(e) {
  let t, r;
  const n = (
    /*#slots*/
    e[7].default
  ), i = Je(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = be("svelte-slot"), i && i.c(), Pe(t, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      O(o, t, s), i && i.m(t, null), e[9](t), r = !0;
    },
    p(o, s) {
      i && i.p && (!r || s & /*$$scope*/
      64) && nt(
        i,
        n,
        o,
        /*$$scope*/
        o[6],
        r ? Ve(
          n,
          /*$$scope*/
          o[6],
          s,
          null
        ) : Xe(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      r || (R(i, o), r = !0);
    },
    o(o) {
      W(i, o), r = !1;
    },
    d(o) {
      o && I(t), i && i.d(o), e[9](null);
    }
  };
}
function ct(e) {
  let t, r, n, i, o = (
    /*$$slots*/
    e[4].default && ie(e)
  );
  return {
    c() {
      t = be("react-portal-target"), r = rt(), o && o.c(), n = Qe(), Pe(t, "class", "svelte-1rt0kpf");
    },
    m(s, l) {
      O(s, t, l), e[8](t), O(s, r, l), o && o.m(s, l), O(s, n, l), i = !0;
    },
    p(s, [l]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, l), l & /*$$slots*/
      16 && R(o, 1)) : (o = ie(s), o.c(), R(o, 1), o.m(n.parentNode, n)) : o && ($e(), W(o, 1, 1, () => {
        o = null;
      }), qe());
    },
    i(s) {
      i || (R(o), i = !0);
    },
    o(s) {
      W(o), i = !1;
    },
    d(s) {
      s && (I(t), I(r), I(n)), e[8](null), o && o.d(s);
    }
  };
}
function se(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function ut(e, t, r) {
  let n, i, {
    $$slots: o = {},
    $$scope: s
  } = t;
  const l = Ze(o);
  let {
    svelteInit: c
  } = t;
  const h = E(se(t)), u = E();
  ne(e, u, (f) => r(0, n = f));
  const a = E();
  ne(e, a, (f) => r(1, i = f));
  const m = [], T = it("$$ms-gr-antd-react-wrapper"), {
    slotKey: j,
    slotIndex: C,
    subSlotIndex: y
  } = Me() || {}, Oe = c({
    parent: T,
    props: h,
    target: u,
    slot: a,
    slotKey: j,
    slotIndex: C,
    subSlotIndex: y,
    onDestroy(f) {
      m.push(f);
    }
  });
  lt("$$ms-gr-antd-react-wrapper", Oe), ot(() => {
    h.set(se(t));
  }), st(() => {
    m.forEach((f) => f());
  });
  function Re(f) {
    re[f ? "unshift" : "push"](() => {
      n = f, u.set(n);
    });
  }
  function De(f) {
    re[f ? "unshift" : "push"](() => {
      i = f, a.set(i);
    });
  }
  return e.$$set = (f) => {
    r(17, t = te(te({}, t), oe(f))), "svelteInit" in f && r(5, c = f.svelteInit), "$$scope" in f && r(6, s = f.$$scope);
  }, t = oe(t), [n, i, u, a, l, c, s, o, Re, De];
}
class ft extends Ge {
  constructor(t) {
    super(), et(this, t, ut, ct, tt, {
      svelteInit: 5
    });
  }
}
const le = window.ms_globals.rerender, K = window.ms_globals.tree;
function at(e) {
  function t(r) {
    const n = E(), i = new ft({
      ...r,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            slotKey: o.slotKey,
            nodes: []
          }, l = o.parent ?? K;
          return l.nodes = [...l.nodes, s], le({
            createPortal: ee,
            node: K
          }), o.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== n), le({
              createPortal: ee,
              node: K
            });
          }), s;
        },
        ...r.props
      }
    });
    return n.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const _t = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function dt(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return typeof n == "number" && !_t.includes(r) ? t[r] = n + "px" : t[r] = n, t;
  }, {}) : {};
}
function Se(e) {
  const t = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((n) => {
    e.getEventListeners(n).forEach(({
      listener: o,
      type: s,
      useCapture: l
    }) => {
      t.addEventListener(s, o, l);
    });
  });
  const r = Array.from(e.children);
  for (let n = 0; n < r.length; n++) {
    const i = r[n], o = Se(i);
    t.replaceChild(o, t.children[n]);
  }
  return t;
}
function mt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const ht = Ae(({
  slot: e,
  clone: t,
  className: r,
  style: n
}, i) => {
  const o = Ye();
  return pe(() => {
    var h;
    if (!o.current || !e)
      return;
    let s = e;
    function l() {
      let u = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (u = s.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), mt(i, u), r && u.classList.add(...r.split(" ")), n) {
        const a = dt(n);
        Object.keys(a).forEach((m) => {
          u.style[m] = a[m];
        });
      }
    }
    let c = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var a;
        s = Se(e), s.style.display = "contents", l(), (a = o.current) == null || a.appendChild(s);
      };
      u(), c = new window.MutationObserver(() => {
        var a, m;
        (a = o.current) != null && a.contains(s) && ((m = o.current) == null || m.removeChild(s)), u();
      }), c.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", l(), (h = o.current) == null || h.appendChild(s);
    return () => {
      var u, a;
      s.style.display = "", (u = o.current) != null && u.contains(s) && ((a = o.current) == null || a.removeChild(s)), c == null || c.disconnect();
    };
  }, [e, t, r, n, i]), he.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  });
});
function pt(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ce(e) {
  return xe(() => pt(e), [e]);
}
var ve = Symbol.for("immer-nothing"), ue = Symbol.for("immer-draftable"), _ = Symbol.for("immer-state");
function p(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var P = Object.getPrototypeOf;
function S(e) {
  return !!e && !!e[_];
}
function w(e) {
  var t;
  return e ? ke(e) || Array.isArray(e) || !!e[ue] || !!((t = e.constructor) != null && t[ue]) || M(e) || L(e) : !1;
}
var yt = Object.prototype.constructor.toString();
function ke(e) {
  if (!e || typeof e != "object") return !1;
  const t = P(e);
  if (t === null)
    return !0;
  const r = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return r === Object ? !0 : typeof r == "function" && Function.toString.call(r) === yt;
}
function D(e, t) {
  F(e) === 0 ? Reflect.ownKeys(e).forEach((r) => {
    t(r, e[r], e);
  }) : e.forEach((r, n) => t(n, r, e));
}
function F(e) {
  const t = e[_];
  return t ? t.type_ : Array.isArray(e) ? 1 : M(e) ? 2 : L(e) ? 3 : 0;
}
function G(e, t) {
  return F(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function Ce(e, t, r) {
  const n = F(e);
  n === 2 ? e.set(t, r) : n === 3 ? e.add(r) : e[t] = r;
}
function gt(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function M(e) {
  return e instanceof Map;
}
function L(e) {
  return e instanceof Set;
}
function g(e) {
  return e.copy_ || e.base_;
}
function q(e, t) {
  if (M(e))
    return new Map(e);
  if (L(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const r = ke(e);
  if (t === !0 || t === "class_only" && !r) {
    const n = Object.getOwnPropertyDescriptors(e);
    delete n[_];
    let i = Reflect.ownKeys(n);
    for (let o = 0; o < i.length; o++) {
      const s = i[o], l = n[s];
      l.writable === !1 && (l.writable = !0, l.configurable = !0), (l.get || l.set) && (n[s] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: l.enumerable,
        value: e[s]
      });
    }
    return Object.create(P(e), n);
  } else {
    const n = P(e);
    if (n !== null && r)
      return {
        ...e
      };
    const i = Object.create(n);
    return Object.assign(i, e);
  }
}
function V(e, t = !1) {
  return N(e) || S(e) || !w(e) || (F(e) > 1 && (e.set = e.add = e.clear = e.delete = wt), Object.freeze(e), t && Object.entries(e).forEach(([r, n]) => V(n, !0))), e;
}
function wt() {
  p(2);
}
function N(e) {
  return Object.isFrozen(e);
}
var bt = {};
function b(e) {
  const t = bt[e];
  return t || p(0, e), t;
}
var v;
function Ee() {
  return v;
}
function Pt(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function fe(e, t) {
  t && (b("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function Z(e) {
  J(e), e.drafts_.forEach(St), e.drafts_ = null;
}
function J(e) {
  e === v && (v = e.parent_);
}
function ae(e) {
  return v = Pt(v, e);
}
function St(e) {
  const t = e[_];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function _e(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const r = t.drafts_[0];
  return e !== void 0 && e !== r ? (r[_].modified_ && (Z(t), p(4)), w(e) && (e = A(t, e), t.parent_ || Y(t, e)), t.patches_ && b("Patches").generateReplacementPatches_(r[_].base_, e, t.patches_, t.inversePatches_)) : e = A(t, r, []), Z(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== ve ? e : void 0;
}
function A(e, t, r) {
  if (N(t)) return t;
  const n = t[_];
  if (!n)
    return D(t, (i, o) => de(e, n, t, i, o, r)), t;
  if (n.scope_ !== e) return t;
  if (!n.modified_)
    return Y(e, n.base_, !0), n.base_;
  if (!n.finalized_) {
    n.finalized_ = !0, n.scope_.unfinalizedDrafts_--;
    const i = n.copy_;
    let o = i, s = !1;
    n.type_ === 3 && (o = new Set(i), i.clear(), s = !0), D(o, (l, c) => de(e, n, i, l, c, r, s)), Y(e, i, !1), r && e.patches_ && b("Patches").generatePatches_(n, r, e.patches_, e.inversePatches_);
  }
  return n.copy_;
}
function de(e, t, r, n, i, o, s) {
  if (S(i)) {
    const l = o && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !G(t.assigned_, n) ? o.concat(n) : void 0, c = A(e, i, l);
    if (Ce(r, n, c), S(c))
      e.canAutoFreeze_ = !1;
    else return;
  } else s && r.add(i);
  if (w(i) && !N(i)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    A(e, i), (!t || !t.scope_.parent_) && typeof n != "symbol" && Object.prototype.propertyIsEnumerable.call(r, n) && Y(e, i);
  }
}
function Y(e, t, r = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && V(t, r);
}
function vt(e, t) {
  const r = Array.isArray(e), n = {
    type_: r ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : Ee(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let i = n, o = $;
  r && (i = [n], o = k);
  const {
    revoke: s,
    proxy: l
  } = Proxy.revocable(i, o);
  return n.draft_ = l, n.revoke_ = s, l;
}
var $ = {
  get(e, t) {
    if (t === _) return e;
    const r = g(e);
    if (!G(r, t))
      return kt(e, r, t);
    const n = r[t];
    return e.finalized_ || !w(n) ? n : n === U(e.base_, t) ? (B(e), e.copy_[t] = X(n, e)) : n;
  },
  has(e, t) {
    return t in g(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(g(e));
  },
  set(e, t, r) {
    const n = ze(g(e), t);
    if (n != null && n.set)
      return n.set.call(e.draft_, r), !0;
    if (!e.modified_) {
      const i = U(g(e), t), o = i == null ? void 0 : i[_];
      if (o && o.base_ === r)
        return e.copy_[t] = r, e.assigned_[t] = !1, !0;
      if (gt(r, i) && (r !== void 0 || G(e.base_, t))) return !0;
      B(e), Q(e);
    }
    return e.copy_[t] === r && // special case: handle new props with value 'undefined'
    (r !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(r) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = r, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return U(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, B(e), Q(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const r = g(e), n = Reflect.getOwnPropertyDescriptor(r, t);
    return n && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: n.enumerable,
      value: r[t]
    };
  },
  defineProperty() {
    p(11);
  },
  getPrototypeOf(e) {
    return P(e.base_);
  },
  setPrototypeOf() {
    p(12);
  }
}, k = {};
D($, (e, t) => {
  k[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
k.deleteProperty = function(e, t) {
  return k.set.call(this, e, t, void 0);
};
k.set = function(e, t, r) {
  return $.set.call(this, e[0], t, r, e[0]);
};
function U(e, t) {
  const r = e[_];
  return (r ? g(r) : e)[t];
}
function kt(e, t, r) {
  var i;
  const n = ze(t, r);
  return n ? "value" in n ? n.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (i = n.get) == null ? void 0 : i.call(e.draft_)
  ) : void 0;
}
function ze(e, t) {
  if (!(t in e)) return;
  let r = P(e);
  for (; r; ) {
    const n = Object.getOwnPropertyDescriptor(r, t);
    if (n) return n;
    r = P(r);
  }
}
function Q(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && Q(e.parent_));
}
function B(e) {
  e.copy_ || (e.copy_ = q(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var Ct = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, r, n) => {
      if (typeof t == "function" && typeof r != "function") {
        const o = r;
        r = t;
        const s = this;
        return function(c = o, ...h) {
          return s.produce(c, (u) => r.call(this, u, ...h));
        };
      }
      typeof r != "function" && p(6), n !== void 0 && typeof n != "function" && p(7);
      let i;
      if (w(t)) {
        const o = ae(this), s = X(t, void 0);
        let l = !0;
        try {
          i = r(s), l = !1;
        } finally {
          l ? Z(o) : J(o);
        }
        return fe(o, n), _e(i, o);
      } else if (!t || typeof t != "object") {
        if (i = r(t), i === void 0 && (i = t), i === ve && (i = void 0), this.autoFreeze_ && V(i, !0), n) {
          const o = [], s = [];
          b("Patches").generateReplacementPatches_(t, i, o, s), n(o, s);
        }
        return i;
      } else p(1, t);
    }, this.produceWithPatches = (t, r) => {
      if (typeof t == "function")
        return (s, ...l) => this.produceWithPatches(s, (c) => t(c, ...l));
      let n, i;
      return [this.produce(t, r, (s, l) => {
        n = s, i = l;
      }), n, i];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    w(e) || p(8), S(e) && (e = Et(e));
    const t = ae(this), r = X(e, void 0);
    return r[_].isManual_ = !0, J(t), r;
  }
  finishDraft(e, t) {
    const r = e && e[_];
    (!r || !r.isManual_) && p(9);
    const {
      scope_: n
    } = r;
    return fe(n, t), _e(void 0, n);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let r;
    for (r = t.length - 1; r >= 0; r--) {
      const i = t[r];
      if (i.path.length === 0 && i.op === "replace") {
        e = i.value;
        break;
      }
    }
    r > -1 && (t = t.slice(r + 1));
    const n = b("Patches").applyPatches_;
    return S(e) ? n(e, t) : this.produce(e, (i) => n(i, t));
  }
};
function X(e, t) {
  const r = M(e) ? b("MapSet").proxyMap_(e, t) : L(e) ? b("MapSet").proxySet_(e, t) : vt(e, t);
  return (t ? t.scope_ : Ee()).drafts_.push(r), r;
}
function Et(e) {
  return S(e) || p(10, e), Ie(e);
}
function Ie(e) {
  if (!w(e) || N(e)) return e;
  const t = e[_];
  let r;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, r = q(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    r = q(e, !0);
  return D(r, (n, i) => {
    Ce(r, n, Ie(i));
  }), t && (t.finalized_ = !1), r;
}
var d = new Ct(), zt = d.produce;
d.produceWithPatches.bind(d);
d.setAutoFreeze.bind(d);
d.setUseStrictShallowCopy.bind(d);
d.applyPatches.bind(d);
d.createDraft.bind(d);
d.finishDraft.bind(d);
var It = {
  exports: {}
};
(function(e, t) {
  (function(r, n) {
    e.exports = n(ye);
  })(Le, function(r) {
    function n(s) {
      return s && typeof s == "object" && "default" in s ? s : {
        default: s
      };
    }
    var i = n(r), o = {
      name: "zh-cn",
      weekdays: "星期日_星期一_星期二_星期三_星期四_星期五_星期六".split("_"),
      weekdaysShort: "周日_周一_周二_周三_周四_周五_周六".split("_"),
      weekdaysMin: "日_一_二_三_四_五_六".split("_"),
      months: "一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月".split("_"),
      monthsShort: "1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),
      ordinal: function(s, l) {
        return l === "W" ? s + "周" : s + "日";
      },
      weekStart: 1,
      yearStart: 4,
      formats: {
        LT: "HH:mm",
        LTS: "HH:mm:ss",
        L: "YYYY/MM/DD",
        LL: "YYYY年M月D日",
        LLL: "YYYY年M月D日Ah点mm分",
        LLLL: "YYYY年M月D日ddddAh点mm分",
        l: "YYYY/M/D",
        ll: "YYYY年M月D日",
        lll: "YYYY年M月D日 HH:mm",
        llll: "YYYY年M月D日dddd HH:mm"
      },
      relativeTime: {
        future: "%s内",
        past: "%s前",
        s: "几秒",
        m: "1 分钟",
        mm: "%d 分钟",
        h: "1 小时",
        hh: "%d 小时",
        d: "1 天",
        dd: "%d 天",
        M: "1 个月",
        MM: "%d 个月",
        y: "1 年",
        yy: "%d 年"
      },
      meridiem: function(s, l) {
        var c = 100 * s + l;
        return c < 600 ? "凌晨" : c < 900 ? "早上" : c < 1100 ? "上午" : c < 1300 ? "中午" : c < 1800 ? "下午" : "晚上";
      }
    };
    return i.default.locale(o, null, !0), o;
  });
})(It);
const me = {
  ar_EG: () => import("./ar_EG-CRvxilkj.js").then((e) => e.a),
  az_AZ: () => import("./az_AZ-DmYuQD0g.js").then((e) => e.a),
  bg_BG: () => import("./bg_BG-Cm_M7C7m.js").then((e) => e.b),
  bn_BD: () => import("./bn_BD-ChEejmcK.js").then((e) => e.b),
  by_BY: () => import("./by_BY-DlO-9xN5.js").then((e) => e.b),
  ca_ES: () => import("./ca_ES-C_ntOx1K.js").then((e) => e.c),
  cs_CZ: () => import("./cs_CZ-DPIwQdMB.js").then((e) => e.c),
  da_DK: () => import("./da_DK-SQs2sQDk.js").then((e) => e.d),
  de_DE: () => import("./de_DE-C1waJIeN.js").then((e) => e.d),
  el_GR: () => import("./el_GR-8cfiezbG.js").then((e) => e.e),
  en_GB: () => import("./en_GB-BLjjn-g2.js").then((e) => e.e),
  en_US: () => import("./en_US-CsDRVix-.js").then((e) => e.e),
  es_ES: () => import("./es_ES-KxNaTlWV.js").then((e) => e.e),
  et_EE: () => import("./et_EE-CAgYL4Jy.js").then((e) => e.e),
  eu_ES: () => import("./eu_ES-CEwXOND1.js").then((e) => e.e),
  fa_IR: () => import("./fa_IR-Ji17Ecz5.js").then((e) => e.f),
  fi_FI: () => import("./fi_FI-Cjbb8XoO.js").then((e) => e.f),
  fr_BE: () => import("./fr_BE-CPtGaDj8.js").then((e) => e.f),
  fr_CA: () => import("./fr_CA-DEkZiY0V.js").then((e) => e.f),
  fr_FR: () => import("./fr_FR-CpLZAgrd.js").then((e) => e.f),
  ga_IE: () => import("./ga_IE-pWoHImE9.js").then((e) => e.g),
  gl_ES: () => import("./gl_ES-BAApdjwm.js").then((e) => e.g),
  he_IL: () => import("./he_IL-BwTG9Kcs.js").then((e) => e.h),
  hi_IN: () => import("./hi_IN-Dh1KZnFL.js").then((e) => e.h),
  hr_HR: () => import("./hr_HR-B-34e1hD.js").then((e) => e.h),
  hu_HU: () => import("./hu_HU-C6UmJuIP.js").then((e) => e.h),
  hy_AM: () => import("./hy_AM-mxENJ2xJ.js").then((e) => e.h),
  id_ID: () => import("./id_ID-DJ4LmCZS.js").then((e) => e.i),
  is_IS: () => import("./is_IS-ClX4hhuq.js").then((e) => e.i),
  it_IT: () => import("./it_IT-Cgsk5-rS.js").then((e) => e.i),
  ja_JP: () => import("./ja_JP-nsEwkyRI.js").then((e) => e.j),
  ka_GE: () => import("./ka_GE-DPkAyW7-.js").then((e) => e.k),
  kk_KZ: () => import("./kk_KZ-ByMqE3Pc.js").then((e) => e.k),
  km_KH: () => import("./km_KH-YzD-AFzQ.js").then((e) => e.k),
  kmr_IQ: () => import("./kmr_IQ-Ttx3aKVk.js").then((e) => e.k),
  kn_IN: () => import("./kn_IN-CIFtV57t.js").then((e) => e.k),
  ko_KR: () => import("./ko_KR-ClZbZoR6.js").then((e) => e.k),
  ku_IQ: () => import("./ku_IQ-vRYQZE9v.js").then((e) => e.k),
  lt_LT: () => import("./lt_LT-Fo6mmUUS.js").then((e) => e.l),
  lv_LV: () => import("./lv_LV-DOqVO1OT.js").then((e) => e.l),
  mk_MK: () => import("./mk_MK-DiT383TQ.js").then((e) => e.m),
  ml_IN: () => import("./ml_IN-Bsh7z9rk.js").then((e) => e.m),
  mn_MN: () => import("./mn_MN-Du0-02as.js").then((e) => e.m),
  ms_MY: () => import("./ms_MY-WpBX7-gI.js").then((e) => e.m),
  my_MM: () => import("./my_MM-CGXJVz8t.js").then((e) => e.m),
  nb_NO: () => import("./nb_NO-B55WCurH.js").then((e) => e.n),
  ne_NP: () => import("./ne_NP-C1grkE0K.js").then((e) => e.n),
  nl_BE: () => import("./nl_BE-CSDGrmKD.js").then((e) => e.n),
  nl_NL: () => import("./nl_NL-B77UjFYu.js").then((e) => e.n),
  pl_PL: () => import("./pl_PL-DjyX8CIl.js").then((e) => e.p),
  pt_BR: () => import("./pt_BR-C9FcUHAW.js").then((e) => e.p),
  pt_PT: () => import("./pt_PT-BBCyz0jb.js").then((e) => e.p),
  ro_RO: () => import("./ro_RO-L4voSsdd.js").then((e) => e.r),
  ru_RU: () => import("./ru_RU-BI5Pa7hE.js").then((e) => e.r),
  si_LK: () => import("./si_LK-Brou43Nd.js").then((e) => e.s),
  sk_SK: () => import("./sk_SK-CIAQWLYR.js").then((e) => e.s),
  sl_SI: () => import("./sl_SI-DKf0pP1P.js").then((e) => e.s),
  sr_RS: () => import("./sr_RS-a87nf6H5.js").then((e) => e.s),
  sv_SE: () => import("./sv_SE-Piuq-Gy4.js").then((e) => e.s),
  ta_IN: () => import("./ta_IN-CtAqUp22.js").then((e) => e.t),
  th_TH: () => import("./th_TH-Oh1WKTj2.js").then((e) => e.t),
  tk_TK: () => import("./tk_TK-Dy0BKbwv.js").then((e) => e.t),
  tr_TR: () => import("./tr_TR-B-xOElGs.js").then((e) => e.t),
  uk_UA: () => import("./uk_UA-B4NYe_gO.js").then((e) => e.u),
  ur_PK: () => import("./ur_PK-BNTxonXb.js").then((e) => e.u),
  uz_UZ: () => import("./uz_UZ-cqZu_BfT.js").then((e) => e.u),
  vi_VN: () => import("./vi_VN-YfZeZ2Al.js").then((e) => e.v),
  zh_CN: () => import("./zh_CN-KN6bawuC.js").then((e) => e.z),
  zh_HK: () => import("./zh_HK-DwDbhzWR.js").then((e) => e.z),
  zh_TW: () => import("./zh_TW-DQt-NlOF.js").then((e) => e.z)
}, Ot = (e, t) => zt(e, (r) => {
  Object.keys(t).forEach((n) => {
    const i = n.split(".");
    let o = r;
    for (let s = 0; s < i.length - 1; s++) {
      const l = i[s];
      o[l] || (o[l] = {}), o = o[l];
    }
    o[i[i.length - 1]] = /* @__PURE__ */ z.jsx(ht, {
      slot: t[n],
      clone: !0
    });
  });
}), Dt = at(({
  slots: e,
  theme_mode: t,
  id: r,
  className: n,
  style: i,
  locale: o,
  getTargetContainer: s,
  getPopupContainer: l,
  children: c,
  ...h
}) => {
  var C;
  const [u, a] = Fe(), m = {
    dark: t === "dark",
    ...((C = h.theme) == null ? void 0 : C.algorithm) || {}
  }, T = ce(l), j = ce(s);
  return pe(() => {
    o && me[o] && me[o]().then((y) => {
      a(y.default), o === "zh_CN" && ye.locale("zh-cn");
    });
  }, [o]), /* @__PURE__ */ z.jsx("div", {
    id: r,
    className: n,
    style: i,
    children: /* @__PURE__ */ z.jsx(Ne, {
      hashPriority: "high",
      container: document.body,
      children: /* @__PURE__ */ z.jsx(Te, {
        prefixCls: "ms-gr-ant",
        ...Ot(h, e),
        locale: u,
        getPopupContainer: T,
        getTargetContainer: j,
        theme: {
          cssVar: !0,
          ...h.theme,
          algorithm: Object.keys(m).map((y) => {
            switch (y) {
              case "dark":
                return m[y] ? H.darkAlgorithm : H.defaultAlgorithm;
              case "compact":
                return m[y] ? H.compactAlgorithm : null;
              default:
                return null;
            }
          }).filter(Boolean)
        },
        children: c
      })
    })
  });
});
export {
  Dt as ConfigProvider,
  Dt as default
};
