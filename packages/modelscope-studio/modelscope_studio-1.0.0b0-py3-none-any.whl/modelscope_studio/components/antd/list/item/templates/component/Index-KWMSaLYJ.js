async function M() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function V(e) {
  return await M(), e().then((t) => t.default);
}
function z(e) {
  const {
    gradio: t,
    _internal: o,
    ...n
  } = e;
  return Object.keys(o).reduce((i, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], r = c.split("_"), a = (..._) => {
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
        return t.dispatch(c.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (r.length > 1) {
        let _ = {
          ...n.props[r[0]] || {}
        };
        i[r[0]] = _;
        for (let u = 1; u < r.length - 1; u++) {
          const m = {
            ...n.props[r[u]] || {}
          };
          _[r[u]] = m, _ = m;
        }
        const p = r[r.length - 1];
        return _[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = a, i;
      }
      const d = r[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = a;
    }
    return i;
  }, {});
}
function v() {
}
function Z(e) {
  return e();
}
function G(e) {
  e.forEach(Z);
}
function H(e) {
  return typeof e == "function";
}
function J(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function L(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return v;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function k(e) {
  let t;
  return L(e, (o) => t = o)(), t;
}
const C = [];
function Q(e, t) {
  return {
    subscribe: g(e, t).subscribe
  };
}
function g(e, t = v) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if (J(e, c) && (e = c, o)) {
      const r = !C.length;
      for (const a of n)
        a[1](), C.push(a, e);
      if (r) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function s(c) {
    i(c(e));
  }
  function l(c, r = v) {
    const a = [c, r];
    return n.add(a), n.size === 1 && (o = t(i, s) || v), c(e), () => {
      n.delete(a), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: l
  };
}
function je(e, t, o) {
  const n = !Array.isArray(e), i = n ? [e] : e;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const s = t.length < 2;
  return Q(o, (l, c) => {
    let r = !1;
    const a = [];
    let d = 0, _ = v;
    const p = () => {
      if (d)
        return;
      _();
      const m = t(n ? a[0] : a, l, c);
      s ? l(m) : _ = H(m) ? m : v;
    }, u = i.map((m, h) => L(m, (w) => {
      a[h] = w, d &= ~(1 << h), r && p();
    }, () => {
      d |= 1 << h;
    }));
    return r = !0, p(), function() {
      G(u), _(), r = !1;
    };
  });
}
const {
  getContext: j,
  setContext: E
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const e = g({});
  return E(T, e);
}
const $ = "$$ms-gr-antd-context-key";
function ee(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = ne(), o = se({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((r) => {
    o.slotKey.set(r);
  }), te();
  const n = j($), i = ((c = k(n)) == null ? void 0 : c.as_item) || e.as_item, s = n ? i ? k(n)[i] : k(n) : {}, l = g({
    ...e,
    ...s
  });
  return n ? (n.subscribe((r) => {
    const {
      as_item: a
    } = k(l);
    a && (r = r[a]), l.update((d) => ({
      ...d,
      ...r
    }));
  }), [l, (r) => {
    const a = r.as_item ? k(n)[r.as_item] : k(n);
    return l.set({
      ...r,
      ...a
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const R = "$$ms-gr-antd-slot-key";
function te() {
  E(R, g(void 0));
}
function ne() {
  return j(R);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function se({
  slot: e,
  index: t,
  subIndex: o
}) {
  return E(U, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(o)
  });
}
function Ee() {
  return j(U);
}
function ie(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var X = {
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
      for (var s = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (s = i(s, n(c)));
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
      for (var c in s)
        t.call(s, c) && s[c] && (l = i(l, c));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(X);
var oe = X.exports;
const A = /* @__PURE__ */ ie(oe), {
  SvelteComponent: le,
  assign: re,
  check_outros: ce,
  component_subscribe: x,
  create_component: ue,
  create_slot: ae,
  destroy_component: fe,
  detach: Y,
  empty: B,
  flush: y,
  get_all_dirty_from_scope: _e,
  get_slot_changes: me,
  get_spread_object: O,
  get_spread_update: de,
  group_outros: pe,
  handle_promise: be,
  init: he,
  insert: D,
  mount_component: ye,
  noop: b,
  safe_not_equal: ge,
  transition_in: K,
  transition_out: S,
  update_await_block_branch: we,
  update_slot_base: ke
} = window.__gradio__svelte__internal;
function q(e) {
  let t, o, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Se,
    then: ve,
    catch: Ce,
    value: 18,
    blocks: [, , ,]
  };
  return be(
    /*AwaitedListItem*/
    e[2],
    n
  ), {
    c() {
      t = B(), n.block.c();
    },
    m(i, s) {
      D(i, t, s), n.block.m(i, n.anchor = s), n.mount = () => t.parentNode, n.anchor = t, o = !0;
    },
    p(i, s) {
      e = i, we(n, e, s);
    },
    i(i) {
      o || (K(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        S(l);
      }
      o = !1;
    },
    d(i) {
      i && Y(t), n.block.d(i), n.token = null, n = null;
    }
  };
}
function Ce(e) {
  return {
    c: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function ve(e) {
  let t, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: A(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-list-item"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].props,
    z(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Ke]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = re(i, n[s]);
  return t = new /*ListItem*/
  e[18]({
    props: i
  }), {
    c() {
      ue(t.$$.fragment);
    },
    m(s, l) {
      ye(t, s, l), o = !0;
    },
    p(s, l) {
      const c = l & /*$mergedProps, $slots*/
      3 ? de(n, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: A(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-list-item"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && O(
        /*$mergedProps*/
        s[0].props
      ), l & /*$mergedProps*/
      1 && O(z(
        /*$mergedProps*/
        s[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }]) : {};
      l & /*$$scope*/
      65536 && (c.$$scope = {
        dirty: l,
        ctx: s
      }), t.$set(c);
    },
    i(s) {
      o || (K(t.$$.fragment, s), o = !0);
    },
    o(s) {
      S(t.$$.fragment, s), o = !1;
    },
    d(s) {
      fe(t, s);
    }
  };
}
function Ke(e) {
  let t;
  const o = (
    /*#slots*/
    e[15].default
  ), n = ae(
    o,
    e,
    /*$$scope*/
    e[16],
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
      65536) && ke(
        n,
        o,
        i,
        /*$$scope*/
        i[16],
        t ? me(
          o,
          /*$$scope*/
          i[16],
          s,
          null
        ) : _e(
          /*$$scope*/
          i[16]
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
function Se(e) {
  return {
    c: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function Pe(e) {
  let t, o, n = (
    /*$mergedProps*/
    e[0].visible && q(e)
  );
  return {
    c() {
      n && n.c(), t = B();
    },
    m(i, s) {
      n && n.m(i, s), D(i, t, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && K(n, 1)) : (n = q(i), n.c(), K(n, 1), n.m(t.parentNode, t)) : n && (pe(), S(n, 1, 1, () => {
        n = null;
      }), ce());
    },
    i(i) {
      o || (K(n), o = !0);
    },
    o(i) {
      S(n), o = !1;
    },
    d(i) {
      i && Y(t), n && n.d(i);
    }
  };
}
function xe(e, t, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: c
  } = t;
  const r = V(() => import("./list.item-CiJl2ibj.js"));
  let {
    gradio: a
  } = t, {
    _internal: d = {}
  } = t, {
    as_item: _
  } = t, {
    props: p = {}
  } = t;
  const u = g(p);
  x(e, u, (f) => o(14, n = f));
  let {
    elem_id: m = ""
  } = t, {
    elem_classes: h = []
  } = t, {
    elem_style: w = {}
  } = t, {
    visible: P = !0
  } = t;
  const [I, F] = ee({
    gradio: a,
    props: n,
    _internal: d,
    as_item: _,
    visible: P,
    elem_id: m,
    elem_classes: h,
    elem_style: w
  });
  x(e, I, (f) => o(0, i = f));
  const N = W();
  return x(e, N, (f) => o(1, s = f)), e.$$set = (f) => {
    "gradio" in f && o(6, a = f.gradio), "_internal" in f && o(7, d = f._internal), "as_item" in f && o(8, _ = f.as_item), "props" in f && o(9, p = f.props), "elem_id" in f && o(10, m = f.elem_id), "elem_classes" in f && o(11, h = f.elem_classes), "elem_style" in f && o(12, w = f.elem_style), "visible" in f && o(13, P = f.visible), "$$scope" in f && o(16, c = f.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    512 && u.update((f) => ({
      ...f,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, as_item, visible, elem_id, elem_classes, elem_style*/
    32192 && F({
      gradio: a,
      props: n,
      _internal: d,
      as_item: _,
      visible: P,
      elem_id: m,
      elem_classes: h,
      elem_style: w
    });
  }, [i, s, r, u, I, N, a, d, _, p, m, h, w, P, n, l, c];
}
class Ie extends le {
  constructor(t) {
    super(), he(this, t, xe, Pe, ge, {
      gradio: 6,
      _internal: 7,
      as_item: 8,
      props: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12,
      visible: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
}
export {
  Ie as I,
  k as a,
  je as d,
  Ee as g,
  g as w
};
