async function T() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function Z(e) {
  return await T(), e().then((t) => t.default);
}
function A(e) {
  const {
    gradio: t,
    _internal: o,
    ...n
  } = e;
  return Object.keys(o).reduce((i, s) => {
    const r = s.match(/bind_(.+)_event/);
    if (r) {
      const a = r[1], l = a.split("_"), f = (..._) => {
        const b = _.map((c) => _ && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        return t.dispatch(a.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (l.length > 1) {
        let _ = {
          ...n.props[l[0]] || {}
        };
        i[l[0]] = _;
        for (let c = 1; c < l.length - 1; c++) {
          const m = {
            ...n.props[l[c]] || {}
          };
          _[l[c]] = m, _ = m;
        }
        const b = l[l.length - 1];
        return _[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, i;
      }
      const d = l[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function C() {
}
function G(e) {
  return e();
}
function H(e) {
  e.forEach(G);
}
function J(e) {
  return typeof e == "function";
}
function Q(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function R(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return C;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function v(e) {
  let t;
  return R(e, (o) => t = o)(), t;
}
const k = [];
function W(e, t) {
  return {
    subscribe: y(e, t).subscribe
  };
}
function y(e, t = C) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(a) {
    if (Q(e, a) && (e = a, o)) {
      const l = !k.length;
      for (const f of n)
        f[1](), k.push(f, e);
      if (l) {
        for (let f = 0; f < k.length; f += 2)
          k[f][0](k[f + 1]);
        k.length = 0;
      }
    }
  }
  function s(a) {
    i(a(e));
  }
  function r(a, l = C) {
    const f = [a, l];
    return n.add(f), n.size === 1 && (o = t(i, s) || C), a(e), () => {
      n.delete(f), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: r
  };
}
function ze(e, t, o) {
  const n = !Array.isArray(e), i = n ? [e] : e;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const s = t.length < 2;
  return W(o, (r, a) => {
    let l = !1;
    const f = [];
    let d = 0, _ = C;
    const b = () => {
      if (d)
        return;
      _();
      const m = t(n ? f[0] : f, r, a);
      s ? r(m) : _ = J(m) ? m : C;
    }, c = i.map((m, g) => R(m, (w) => {
      f[g] = w, d &= ~(1 << g), l && b();
    }, () => {
      d |= 1 << g;
    }));
    return l = !0, b(), function() {
      H(c), _(), l = !1;
    };
  });
}
const {
  getContext: N,
  setContext: z
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const e = y({});
  return z($, e);
}
const te = "$$ms-gr-antd-context-key";
function ne(e) {
  var a;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = oe(), o = ie({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((l) => {
    o.slotKey.set(l);
  }), se();
  const n = N(te), i = ((a = v(n)) == null ? void 0 : a.as_item) || e.as_item, s = n ? i ? v(n)[i] : v(n) : {}, r = y({
    ...e,
    ...s
  });
  return n ? (n.subscribe((l) => {
    const {
      as_item: f
    } = v(r);
    f && (l = l[f]), r.update((d) => ({
      ...d,
      ...l
    }));
  }), [r, (l) => {
    const f = l.as_item ? v(n)[l.as_item] : v(n);
    return r.set({
      ...l,
      ...f
    });
  }]) : [r, (l) => {
    r.set(l);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function se() {
  z(U, y(void 0));
}
function oe() {
  return N(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: e,
  index: t,
  subIndex: o
}) {
  return z(X, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(o)
  });
}
function Ie() {
  return N(X);
}
function re(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Y = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var s = "", r = 0; r < arguments.length; r++) {
        var a = arguments[r];
        a && (s = i(s, n(a)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return o.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var r = "";
      for (var a in s)
        t.call(s, a) && s[a] && (r = i(r, a));
      return r;
    }
    function i(s, r) {
      return r ? s ? s + " " + r : s + r : s;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(Y);
var le = Y.exports;
const O = /* @__PURE__ */ re(le), {
  SvelteComponent: ce,
  assign: ue,
  check_outros: ae,
  component_subscribe: E,
  create_component: fe,
  create_slot: _e,
  destroy_component: me,
  detach: B,
  empty: D,
  flush: h,
  get_all_dirty_from_scope: de,
  get_slot_changes: be,
  get_spread_object: q,
  get_spread_update: pe,
  group_outros: he,
  handle_promise: ge,
  init: ye,
  insert: F,
  mount_component: we,
  noop: p,
  safe_not_equal: ve,
  transition_in: K,
  transition_out: S,
  update_await_block_branch: ke,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function V(e) {
  let t, o, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: je,
    then: Se,
    catch: Ke,
    value: 20,
    blocks: [, , ,]
  };
  return ge(
    /*AwaitedTransfer*/
    e[3],
    n
  ), {
    c() {
      t = D(), n.block.c();
    },
    m(i, s) {
      F(i, t, s), n.block.m(i, n.anchor = s), n.mount = () => t.parentNode, n.anchor = t, o = !0;
    },
    p(i, s) {
      e = i, ke(n, e, s);
    },
    i(i) {
      o || (K(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const r = n.blocks[s];
        S(r);
      }
      o = !1;
    },
    d(i) {
      i && B(t), n.block.d(i), n.token = null, n = null;
    }
  };
}
function Ke(e) {
  return {
    c: p,
    m: p,
    p,
    i: p,
    o: p,
    d: p
  };
}
function Se(e) {
  let t, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: O(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-transfer"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[1].elem_id
      )
    },
    {
      targetKeys: (
        /*$mergedProps*/
        e[1].value
      )
    },
    /*$mergedProps*/
    e[1].props,
    A(
      /*$mergedProps*/
      e[1]
    ),
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      onValueChange: (
        /*func*/
        e[17]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Pe]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = ue(i, n[s]);
  return t = new /*Transfer*/
  e[20]({
    props: i
  }), {
    c() {
      fe(t.$$.fragment);
    },
    m(s, r) {
      we(t, s, r), o = !0;
    },
    p(s, r) {
      const a = r & /*$mergedProps, $slots, value*/
      7 ? pe(n, [r & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, r & /*$mergedProps*/
      2 && {
        className: O(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-transfer"
        )
      }, r & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, r & /*$mergedProps*/
      2 && {
        targetKeys: (
          /*$mergedProps*/
          s[1].value
        )
      }, r & /*$mergedProps*/
      2 && q(
        /*$mergedProps*/
        s[1].props
      ), r & /*$mergedProps*/
      2 && q(A(
        /*$mergedProps*/
        s[1]
      )), r & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }, r & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          s[17]
        )
      }]) : {};
      r & /*$$scope*/
      262144 && (a.$$scope = {
        dirty: r,
        ctx: s
      }), t.$set(a);
    },
    i(s) {
      o || (K(t.$$.fragment, s), o = !0);
    },
    o(s) {
      S(t.$$.fragment, s), o = !1;
    },
    d(s) {
      me(t, s);
    }
  };
}
function Pe(e) {
  let t;
  const o = (
    /*#slots*/
    e[16].default
  ), n = _e(
    o,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, s) {
      n && n.m(i, s), t = !0;
    },
    p(i, s) {
      n && n.p && (!t || s & /*$$scope*/
      262144) && Ce(
        n,
        o,
        i,
        /*$$scope*/
        i[18],
        t ? be(
          o,
          /*$$scope*/
          i[18],
          s,
          null
        ) : de(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      t || (K(n, i), t = !0);
    },
    o(i) {
      S(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function je(e) {
  return {
    c: p,
    m: p,
    p,
    i: p,
    o: p,
    d: p
  };
}
function Ee(e) {
  let t, o, n = (
    /*$mergedProps*/
    e[1].visible && V(e)
  );
  return {
    c() {
      n && n.c(), t = D();
    },
    m(i, s) {
      n && n.m(i, s), F(i, t, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[1].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      2 && K(n, 1)) : (n = V(i), n.c(), K(n, 1), n.m(t.parentNode, t)) : n && (he(), S(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(i) {
      o || (K(n), o = !0);
    },
    o(i) {
      S(n), o = !1;
    },
    d(i) {
      i && B(t), n && n.d(i);
    }
  };
}
function Ne(e, t, o) {
  let n, i, s, {
    $$slots: r = {},
    $$scope: a
  } = t;
  const l = Z(() => import("./transfer-fRcowcu0.js"));
  let {
    gradio: f
  } = t, {
    props: d = {}
  } = t;
  const _ = y(d);
  E(e, _, (u) => o(15, n = u));
  let {
    _internal: b = {}
  } = t, {
    value: c
  } = t, {
    as_item: m
  } = t, {
    visible: g = !0
  } = t, {
    elem_id: w = ""
  } = t, {
    elem_classes: P = []
  } = t, {
    elem_style: j = {}
  } = t;
  const [I, L] = ne({
    gradio: f,
    props: n,
    _internal: b,
    visible: g,
    elem_id: w,
    elem_classes: P,
    elem_style: j,
    as_item: m,
    value: c
  });
  E(e, I, (u) => o(1, i = u));
  const x = ee();
  E(e, x, (u) => o(2, s = u));
  const M = (u) => {
    o(0, c = u);
  };
  return e.$$set = (u) => {
    "gradio" in u && o(7, f = u.gradio), "props" in u && o(8, d = u.props), "_internal" in u && o(9, b = u._internal), "value" in u && o(0, c = u.value), "as_item" in u && o(10, m = u.as_item), "visible" in u && o(11, g = u.visible), "elem_id" in u && o(12, w = u.elem_id), "elem_classes" in u && o(13, P = u.elem_classes), "elem_style" in u && o(14, j = u.elem_style), "$$scope" in u && o(18, a = u.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && _.update((u) => ({
      ...u,
      ...d
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65153 && L({
      gradio: f,
      props: n,
      _internal: b,
      visible: g,
      elem_id: w,
      elem_classes: P,
      elem_style: j,
      as_item: m,
      value: c
    });
  }, [c, i, s, l, _, I, x, f, d, b, m, g, w, P, j, n, r, M, a];
}
class xe extends ce {
  constructor(t) {
    super(), ye(this, t, Ne, Ee, ve, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 0,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), h();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), h();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), h();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), h();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), h();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), h();
  }
}
export {
  xe as I,
  v as a,
  ze as d,
  Ie as g,
  y as w
};
