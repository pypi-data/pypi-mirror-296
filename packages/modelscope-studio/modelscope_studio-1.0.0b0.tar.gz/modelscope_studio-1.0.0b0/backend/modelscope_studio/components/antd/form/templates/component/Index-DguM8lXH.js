async function Z() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function B(t) {
  return await Z(), t().then((e) => e.default);
}
function q(t) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = t;
  return Object.keys(o).reduce((i, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const a = l[1], c = a.split("_"), f = (..._) => {
        const p = _.map((u) => _ && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
          type: u.type,
          detail: u.detail,
          timestamp: u.timeStamp,
          clientX: u.clientX,
          clientY: u.clientY,
          targetId: u.target.id,
          targetClassName: u.target.className,
          altKey: u.altKey,
          ctrlKey: u.ctrlKey,
          shiftKey: u.shiftKey,
          metaKey: u.metaKey
        } : u);
        return e.dispatch(a.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (c.length > 1) {
        let _ = {
          ...n.props[c[0]] || {}
        };
        i[c[0]] = _;
        for (let u = 1; u < c.length - 1; u++) {
          const h = {
            ...n.props[c[u]] || {}
          };
          _[c[u]] = h, _ = h;
        }
        const p = c[c.length - 1];
        return _[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, i;
      }
      const d = c[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function j() {
}
function G(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function H(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return j;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(t) {
  let e;
  return H(t, (o) => e = o)(), e;
}
const w = [];
function g(t, e = j) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(a) {
    if (G(t, a) && (t = a, o)) {
      const c = !w.length;
      for (const f of n)
        f[1](), w.push(f, t);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function s(a) {
    i(a(t));
  }
  function l(a, c = j) {
    const f = [a, c];
    return n.add(f), n.size === 1 && (o = e(i, s) || j), a(t), () => {
      n.delete(f), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: l
  };
}
const {
  getContext: z,
  setContext: I
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-slots-key";
function Q() {
  const t = g({});
  return I(J, t);
}
const T = "$$ms-gr-antd-context-key";
function W(t) {
  var a;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ee(), o = te({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    o.slotKey.set(c);
  }), $();
  const n = z(T), i = ((a = y(n)) == null ? void 0 : a.as_item) || t.as_item, s = n ? i ? y(n)[i] : y(n) : {}, l = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: f
    } = y(l);
    f && (c = c[f]), l.update((d) => ({
      ...d,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? y(n)[c.as_item] : y(n);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const F = "$$ms-gr-antd-slot-key";
function $() {
  I(F, g(void 0));
}
function ee() {
  return z(F);
}
const R = "$$ms-gr-antd-component-slot-context-key";
function te({
  slot: t,
  index: e,
  subIndex: o
}) {
  return I(R, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
  });
}
function Pe() {
  return z(R);
}
function ne(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var U = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function o() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var a = arguments[l];
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
      var l = "";
      for (var a in s)
        e.call(s, a) && s[a] && (l = i(l, a));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(U);
var se = U.exports;
const x = /* @__PURE__ */ ne(se), {
  SvelteComponent: oe,
  assign: ie,
  check_outros: le,
  component_subscribe: N,
  create_component: re,
  create_slot: ce,
  destroy_component: ue,
  detach: X,
  empty: Y,
  flush: b,
  get_all_dirty_from_scope: ae,
  get_slot_changes: fe,
  get_spread_object: A,
  get_spread_update: _e,
  group_outros: me,
  handle_promise: de,
  init: be,
  insert: D,
  mount_component: pe,
  noop: m,
  safe_not_equal: he,
  transition_in: k,
  transition_out: v,
  update_await_block_branch: ge,
  update_slot_base: ye
} = window.__gradio__svelte__internal;
function V(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ce,
    then: ke,
    catch: we,
    value: 20,
    blocks: [, , ,]
  };
  return de(
    /*AwaitedForm*/
    t[3],
    n
  ), {
    c() {
      e = Y(), n.block.c();
    },
    m(i, s) {
      D(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, ge(n, t, s);
    },
    i(i) {
      o || (k(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        v(l);
      }
      o = !1;
    },
    d(i) {
      i && X(e), n.block.d(i), n.token = null, n = null;
    }
  };
}
function we(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function ke(t) {
  let e, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        t[1].elem_style
      )
    },
    {
      className: x(
        /*$mergedProps*/
        t[1].elem_classes,
        "ms-gr-antd-form"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[1].elem_id
      )
    },
    /*$mergedProps*/
    t[1].props,
    q(
      /*$mergedProps*/
      t[1]
    ),
    {
      slots: (
        /*$slots*/
        t[2]
      )
    },
    {
      value: (
        /*$mergedProps*/
        t[1].value
      )
    },
    {
      onValueChange: (
        /*func*/
        t[17]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ve]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = ie(i, n[s]);
  return e = new /*Form*/
  t[20]({
    props: i
  }), {
    c() {
      re(e.$$.fragment);
    },
    m(s, l) {
      pe(e, s, l), o = !0;
    },
    p(s, l) {
      const a = l & /*$mergedProps, $slots, value*/
      7 ? _e(n, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: x(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-form"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && A(
        /*$mergedProps*/
        s[1].props
      ), l & /*$mergedProps*/
      2 && A(q(
        /*$mergedProps*/
        s[1]
      )), l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }, l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          s[1].value
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          s[17]
        )
      }]) : {};
      l & /*$$scope*/
      262144 && (a.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(a);
    },
    i(s) {
      o || (k(e.$$.fragment, s), o = !0);
    },
    o(s) {
      v(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ue(e, s);
    }
  };
}
function ve(t) {
  let e;
  const o = (
    /*#slots*/
    t[16].default
  ), n = ce(
    o,
    t,
    /*$$scope*/
    t[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, s) {
      n && n.m(i, s), e = !0;
    },
    p(i, s) {
      n && n.p && (!e || s & /*$$scope*/
      262144) && ye(
        n,
        o,
        i,
        /*$$scope*/
        i[18],
        e ? fe(
          o,
          /*$$scope*/
          i[18],
          s,
          null
        ) : ae(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      e || (k(n, i), e = !0);
    },
    o(i) {
      v(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Ce(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Ke(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[1].visible && V(t)
  );
  return {
    c() {
      n && n.c(), e = Y();
    },
    m(i, s) {
      n && n.m(i, s), D(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[1].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      2 && k(n, 1)) : (n = V(i), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (me(), v(n, 1, 1, () => {
        n = null;
      }), le());
    },
    i(i) {
      o || (k(n), o = !0);
    },
    o(i) {
      v(n), o = !1;
    },
    d(i) {
      i && X(e), n && n.d(i);
    }
  };
}
function Se(t, e, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: a
  } = e;
  const c = B(() => import("./form-Df8vAXnJ.js"));
  let {
    gradio: f
  } = e, {
    value: d
  } = e, {
    props: _ = {}
  } = e;
  const p = g(_);
  N(t, p, (r) => o(15, n = r));
  let {
    _internal: u = {}
  } = e, {
    as_item: h
  } = e, {
    visible: C = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [E, L] = W({
    gradio: f,
    props: n,
    _internal: u,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    as_item: h,
    value: d
  });
  N(t, E, (r) => o(1, i = r));
  const O = Q();
  N(t, O, (r) => o(2, s = r));
  const M = (r) => {
    o(0, d = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && o(7, f = r.gradio), "value" in r && o(0, d = r.value), "props" in r && o(8, _ = r.props), "_internal" in r && o(9, u = r._internal), "as_item" in r && o(10, h = r.as_item), "visible" in r && o(11, C = r.visible), "elem_id" in r && o(12, K = r.elem_id), "elem_classes" in r && o(13, S = r.elem_classes), "elem_style" in r && o(14, P = r.elem_style), "$$scope" in r && o(18, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    256 && p.update((r) => ({
      ...r,
      ..._
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65153 && L({
      gradio: f,
      props: n,
      _internal: u,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      as_item: h,
      value: d
    });
  }, [d, i, s, c, p, E, O, f, _, u, h, C, K, S, P, n, l, M, a];
}
class je extends oe {
  constructor(e) {
    super(), be(this, e, Se, Ke, he, {
      gradio: 7,
      value: 0,
      props: 8,
      _internal: 9,
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
  set gradio(e) {
    this.$$set({
      gradio: e
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), b();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
}
export {
  je as I,
  Pe as g,
  g as w
};
